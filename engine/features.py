from playsound import playsound
import eel
from engine.config import ASSISTANT_NAME
from engine.command import speak
import os

# Playing Assistant Sound function
@eel.expose
def playAssistantSound():
    music_dir ="www/assets/audio/start_sound.mp3"
    playsound(music_dir)


def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query.lower()

    if query!="":
        speak("Opening"+ query)
        os.system('open -a '+query)  #MAC          
        #os.system('start'+query) #WINDOWS
    else:
        speak("not found")
