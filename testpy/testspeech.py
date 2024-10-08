import pyttsx3

def speak(text):
    try:
        print('trying to speak')
        engine = pyttsx3.init()
        
        # Logging voices to identify which ones are available
        voices = engine.getProperty('voices')
        
        engine.setProperty('voice', voices[14].id)  # Set a known valid voice
        engine.setProperty('rate', 184)  # Set speech rate

        # Try speaking sanitized text and catch any errors
        engine.say(text)
        engine.runAndWait()
        print("Speaking complete.")
    except Exception as e:
        print(f"Error occurred: {str(e)}")

# Test with problematic text
text = 'I \'m an artificial intelligence model known as Llama. Llama stands for "Large Language Model Meta AI."'
speak(text)
