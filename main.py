import os
import eel
import platform

from engine.features import *
from engine.command import *
from engine.auth import recognize
def start():
    eel.init("www")

    playAssistantSound()
    
    @eel.expose
    def init():
        time.sleep(2) #Can do some initializatio like initializing phone support
        eel.hideLoader()
        speak('Ready for face authentication')
        flag = recognize.AuthenticateFace()
        if flag == 1:
            eel.hideFaceAuth()
            speak('Face Authetication Successful')
            eel.hideFaceAuthSuccess()
            speak('Welcome Mr. Dj')
            time.sleep(2)
            eel.hideStart()
        else:
            speak('Face Authentication Fail')
    
    if platform.system() == 'Darwin':
        os.system('open -a /Applications/Safari.app http://localhost:8000/index.html') #MAC
    elif platform.system() == 'Windows':
        os.system('start msedge.exe --app "http://localhost:8000/index.html"') #WINDOWS
    else:
        print("This is another OS")

    eel.start('index.html', mode=None, host='localhost', block=True)
