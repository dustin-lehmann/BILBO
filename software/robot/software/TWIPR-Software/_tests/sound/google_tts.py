import os
import time
import pygame
from gtts import gTTS



def speak(message, lang="en", filename="output.mp3"):
    try:
        # Generate audio file with gTTS
        tts = gTTS(text=message, lang=lang)
        tts.save(filename)

        # Initialize pygame mixer
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play()


        # Wait until the playback finishes
        time.sleep(3)
        while pygame.mixer.music.get_busy():
            continue

        # Remove the file after playback
        os.remove(filename)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    speak("Start stand-alone")
    # speak("Joystick disconnected")
    speak("I am Bilbo 2")
