import os
import eel

eel.init("www")

#os.system('start msedge.exe --app "http://localhost:8000/index.html"') #WINDOWS
os.system('open -a /Applications/Safari.app http://localhost:8000/index.html') #MAC

eel.start('index.html', mode=None, host='localhost', block=True)
