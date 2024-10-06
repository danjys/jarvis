import os
import re
import sqlite3
import struct
import subprocess
from pipes import quote
import time
import webbrowser
from playsound import playsound
import eel
import pyaudio
from engine.config import ASSISTANT_NAME
from engine.command import speak
import pywhatkit as kit
import platform
from engine.helper import extract_yt_term, remove_words
import pvporcupine
import pyautogui as autogui

#loading environment variables from .env files
from dotenv import load_dotenv

load_dotenv()

con = sqlite3.connect('jarvis.db')
cursor = con.cursor()

# Playing Assistant Sound function
@eel.expose
def playAssistantSound():
    music_dir ="www/assets/audio/start_sound.mp3"
    playsound(music_dir)


def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query.lower()

    app_name = query.strip()
    if app_name != "":

        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening"+ query)
                    if platform.system() == 'Darwin':
                        os.system('open -a '+query)  #MAC 
                    elif platform.system() == 'Windows':
                        os.system('start'+query) #WINDOWS
                    else:
                        print("This is another OS")
        except:
            speak("some thing went wrong")

    #if query!="":
    #    speak("Opening"+ query)
    #    if platform.system() == 'Darwin':
    #        os.system('open -a '+query)  #MAC 
    #    elif platform.system() == 'Windows':
    #        os.system('start'+query) #WINDOWS
    #    else:
    #        print("This is another OS")
    #else:
    #    speak("not found")

def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on YouTube")
    kit.playonyt(search_term)

 
def hotword():
    porcupine = None
    paud = None
    audio_stream = None
    access_key = os.getenv('ACCESS_KEY')  # AccessKey obtained from Picovoice Console (https://console.picovoice.ai/)

    try:
        # Pre-trained keywords
        porcupine = pvporcupine.create(access_key=access_key, keywords=["jarvis", "alexa"])
        paud = pyaudio.PyAudio()

        # Increase frames_per_buffer for macOS to avoid input overflow
        frames_per_buffer = porcupine.frame_length * 2 if platform.system() == 'Darwin' else porcupine.frame_length

        audio_stream = paud.open(rate=porcupine.sample_rate, 
                                 channels=1, 
                                 format=pyaudio.paInt16, 
                                 input=True, 
                                 frames_per_buffer=frames_per_buffer)

        # Loop for streaming
        while True:
            try:
                keyword = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)  # Avoid breaking on overflow
                keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)

                # Process keyword from mic
                keyword_index = porcupine.process(keyword)
                if keyword_index >= 0:
                    print("Hotword detected")

                    # Pressing shortcut key (Windows + J for Windows, Command + K for Mac)
                    if platform.system() == 'Darwin':
                        autogui.keyDown("command")
                        autogui.press("j")
                        autogui.keyUp("command")  # MAC
                    elif platform.system() == 'Windows':
                        autogui.keyDown("win")
                        autogui.press("j")
                        autogui.keyUp("win")  # WINDOWS
                    else:
                        print("This is another OS")
            except IOError as e:
                if e.errno == -9981:  # Input overflow error
                    print("Warning: Input overflowed, continuing...")
                    continue  # Skip this iteration and continue
                else:
                    raise

    except Exception as e:
        print(f"Error: {str(e)}")
    
    finally:
        # Ensure resources are cleaned up
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()


# find contacts
def findContact(query):
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])

        if not mobile_number_str.startswith('+1'):
            mobile_number_str = '+1' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0
    
# Whatsapp 
def whatsApp(mobile_no, message, flag, name):
    if flag == 'message':
        target_tab = 12
        jarvis_message = "message send successfully to "+name

    elif flag == 'call':
        target_tab = 7
        message = ''
        jarvis_message = "calling to "+name

    else:
        target_tab = 6
        message = ''
        jarvis_message = "staring video call with "+name


    # Encode the message for URL
    encoded_message = quote(message)
    print(encoded_message)
    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    autogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        autogui.hotkey('tab')

    autogui.hotkey('enter')
    speak(jarvis_message)


def makeCall(name, mobileNo):
    mobileNo =mobileNo.replace(" ", "")
    speak("Calling "+name)
    command = 'adb shell am start -a android.intent.action.CALL -d tel:'+mobileNo
    os.system(command)


# to send message
def sendMessage(message, mobileNo, name):
    from engine.helper import replace_spaces_with_percent_s, goback, keyEvent, tapEvents, adbInput
    message = replace_spaces_with_percent_s(message)
    mobileNo = replace_spaces_with_percent_s(mobileNo)
    speak("sending message")
    goback(4)
    time.sleep(1)
    keyEvent(3)
    # open sms app
    tapEvents(136, 2220)
    #start chat
    tapEvents(819, 2192)
    # search mobile no
    adbInput(mobileNo)
    #tap on name
    tapEvents(601, 574)
    # tap on input
    tapEvents(390, 2270)
    #message
    adbInput(message)
    #send
    tapEvents(957, 1397)
    speak("message send successfully to "+name)