# J.A.R.V.I.S

## REQUIREMENTS
```
pip install --upgrade pip
pip install pyobjc
pip install pyttsx3
pip install SpeechRecognition
pip install PyAudio
pip install pywhatkit
pip install python-dotenv
pip install pvporcupine 
```

### NOTES

db.py create the databases by running the appropriate queries and adding your necessary commands

### VISUAL STUDIO EXTENSIONS 
- NOTES
- Live Server
- Pylance
- SQLite Viewer

### Porcupine 
Porcupine library is used for hot word detection

pip install pvporcupine==1.9.5 //Free Version new versions are paid and jarvis voice is trained. Its an NLP based Library

MACOSX ISSUE
Since you're using the older version pvporcupine==1.9.5, which doesn't natively support Apple Silicon (arm64), there are a couple of approaches you can try to work around the architecture mismatch issue.

//picovoice # AccessKey obtained from [Picovoice Console](https://console.picovoice.ai/)