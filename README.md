# J.A.R.V.I.S

## REQUIREMENTS
``` bash
pip install --upgrade pip
pip install pyobjc
pip install pyttsx3
pip install SpeechRecognition
pip install PyAudio
pip install pywhatkit
pip install python-dotenv
pip install pvporcupine 
pip install hugchat
pip install opencv-python
pip install opencv-contrib-python 
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

> [!CAUTION]
> pip install pvporcupine==1.9.5 //Free Version new versions are paid and jarvis voice is trained. Its an NLP based Library

> [!WARNING]
> MACOSX ISSUE
> Since you're using the older version pvporcupine==1.9.5, which doesn't natively support Apple Silicon (arm64), there are a couple of approaches you can try to work around the architecture mismatch issue.

> [!IMPORTANT]
> //picovoice # AccessKey obtained from [Picovoice Console](https://console.picovoice.ai/)

## USAGE
- `open` an app : opens an app that is installed on the machine
- `open` Youtube : opens a the webpage is this is configured in the sqlite
- Play Thunder by Imagine Dragons `on youtube` : will open youtube and play the song


## HUGCHAT
    - Create account in huggingface.co
    - goto  /chat
    - install cookie export extension after loggin inot it and picking a ai model
    - create file engine/cookies.json and paste cookies json form https://huggingface.co/chat/

## FACE AUTHENTICATION
- Run engine/auth/sample.py to capture samples to train a face
- Run trainer.py to generate a trainer.yml to be used for face authentication
> [!NOTE]
> Uses haarcascade whihc gives 50-60% face detection acuracy but easier to use for web development.


## RESOURCES
> [!TIP]
> - undraw
> - lottie files









