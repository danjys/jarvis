import platform
import struct
import pvporcupine
import pyaudio
import pyautogui as autogui
import os
from dotenv import load_dotenv

load_dotenv()

def hotword():
    porcupine = None
    paud = None
    audio_stream = None
    access_key = os.getenv('ACCESS_KEY')  # AccessKey obtained from Picovoice Console (https://console.picovoice.ai/)

    try:
        # Pre-trained keywords
        porcupine = pvporcupine.create(access_key=access_key, keywords=["jarvis", "alexa"])
        paud = pyaudio.PyAudio()

        # Increase frames_per_buffer for macOS to avoid input overflow
        frames_per_buffer = porcupine.frame_length * 2 if platform.system() == 'Darwin' else porcupine.frame_length

        audio_stream = paud.open(rate=porcupine.sample_rate, 
                                 channels=1, 
                                 format=pyaudio.paInt16, 
                                 input=True, 
                                 frames_per_buffer=frames_per_buffer)

        # Loop for streaming
        while True:
            try:
                keyword = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)  # Avoid breaking on overflow
                keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)

                # Process keyword from mic
                keyword_index = porcupine.process(keyword)
                if keyword_index >= 0:
                    print("Hotword detected")

                    # Pressing shortcut key (Windows + J for Windows, Command + K for Mac)
                    if platform.system() == 'Darwin':
                        autogui.keyDown("command")
                        autogui.press("K")
                        autogui.keyUp("command")  # MAC
                    elif platform.system() == 'Windows':
                        autogui.keyDown("win")
                        autogui.press("j")
                        autogui.keyUp("win")  # WINDOWS
                    else:
                        print("This is another OS")
            except IOError as e:
                if e.errno == -9981:  # Input overflow error
                    print("Warning: Input overflowed, continuing...")
                    continue  # Skip this iteration and continue
                else:
                    raise

    except Exception as e:
        print(f"Error: {str(e)}")
    
    finally:
        # Ensure resources are cleaned up
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()
hotword()