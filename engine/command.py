import pyttsx3


def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')       #getting details of current voice
    engine.setProperty('voice', voices[14].id)   #changing index, changes voices. 1 for female, 8 : computer 
    engine.setProperty('rate', 184)     # setting up new voice rate

    engine.say(text)
    engine.runAndWait()

speak("I Am JARVIS... how are you doing DJ")    