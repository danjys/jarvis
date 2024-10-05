import os
import eel
import platform

from engine.features import *
from engine.command import *

eel.init("www")

playAssistantSound()

if platform.system() == 'Darwin':
    os.system('open -a /Applications/Safari.app http://localhost:8000/index.html') #MAC
elif platform.system() == 'Windows':
    os.system('start msedge.exe --app "http://localhost:8000/index.html"') #WINDOWS
else:
    print("This is another OS")

eel.start('index.html', mode=None, host='localhost', block=True)
