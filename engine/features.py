import os
import re
import sqlite3
import struct
import time
import webbrowser
from playsound import playsound
import eel
import pyaudio
from engine.config import ASSISTANT_NAME
from engine.command import speak
import pywhatkit as kit
import platform
from engine.helper import extract_yt_term
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