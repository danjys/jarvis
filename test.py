import struct
import time
import pvporcupine
import pyaudio
import pyautogui as autogui
import signal
import sys

def hotword():
    porcupine = None
    paud = None
    audio_stream = None
    try:
        # List available audio devices (especially for macOS)
        paud = pyaudio.PyAudio()
        print("Available audio devices:")
        for i in range(paud.get_device_count()):
            device_info = paud.get_device_info_by_index(i)
            print(f"Device {i}: {device_info['name']} - Input Channels: {device_info['maxInputChannels']}")
        
        # Select a suitable input device (you can modify this based on the list output)
        # You may need to change `device_index` to match your system's microphone input device
        device_index = int(input("Select the input device index: "))  # Prompt user to select the device
        input_device_info = paud.get_device_info_by_index(device_index)
        
        print(f"Using device {device_index}: {input_device_info['name']}")

        # Create a Porcupine instance with pre-trained keywords
        porcupine = pvporcupine.create(keywords=["jarvis", "alexa"]) 
        
        # Open the audio stream with selected input device
        audio_stream = paud.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            input_device_index=device_index,  # macOS specific input device
            frames_per_buffer=porcupine.frame_length
        )
        
        print("Listening for hotwords...")

        # Infinite loop to stream audio
        while True:
            # Read the audio stream
            keyword = audio_stream.read(porcupine.frame_length)
            keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)

            # Process the audio and check for hotwords
            keyword_index = porcupine.process(keyword)
            if keyword_index >= 0:
                print(f"Hotword '{['jarvis', 'alexa'][keyword_index]}' detected")

                # Simulate pressing the shortcut key
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Clean up resources
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

# Run the hotword detection
hotword()