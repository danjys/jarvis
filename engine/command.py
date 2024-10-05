import pyttsx3
import speech_recognition as sr
import eel

def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')       #getting details of current voice
    engine.setProperty('voice', voices[14].id)   #changing index, changes voices. 1 for female, 8 : computer 
    engine.setProperty('rate', 184)     # setting up new voice rate

    engine.say(text)
    engine.runAndWait()

@eel.expose
def takecommand():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('listening...')
        eel.DisplayMessage('listening...')
        r.pause_threshold = 1
        #r.energy_threshold = 300  # You can adjust this based on your environme
        r.adjust_for_ambient_noise(source)

        audio = r.listen(source, 10, 6)
        #try:
        #    audio = r.listen(source, phrase_time_limit=6)
        #except sr.WaitTimeoutError:
        #    print("Timeout error, please try again.")
        #    return ""
    
    try:
        print('recognizing...')
        eel.DisplayMessage('recognizing...')
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
        speak(query)
        eel.ShowHood()
    except Exception as e:
        return ""
    
    return query.lower()

#text = takecommand()
#speak(text)    