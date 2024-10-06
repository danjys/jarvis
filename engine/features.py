import os
import re
import sqlite3
import webbrowser
from playsound import playsound
import eel
from engine.config import ASSISTANT_NAME
from engine.command import speak
import pywhatkit as kit
import platform

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

def extract_yt_term(command):
    # Define a regular expression pattern to capture the song name
    pattern = r'play\s+(.*?)\s+on\s+youtube'
    # Use re.search to find the match in the command
    match = re.search(pattern, command, re.IGNORECASE)
    # If a match if found, return the extracted song name; otherwise return None
    return match.group(1) if match else None    