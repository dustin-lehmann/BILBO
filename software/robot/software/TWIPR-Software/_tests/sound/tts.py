import pyttsx3
import queue
import threading
import time

speech_queue = queue.Queue(maxsize=10)  # Limit the queue size to 10 messages
speech_thread = None
stop_thread = False


def setup_tts_engine():
    """
    Configures a new instance of the pyttsx3 TTS engine with a preferred voice and properties.
    """
    engine = pyttsx3.init()

    # Get all available voices
    voices = engine.getProperty('voices')
    for i, voice in enumerate(voices):
        print(f"Voice #{i}: {voice.name} (ID: {voice.id})")
    engine.setProperty('voice', 'English (America)')



    # Try to find a female voice (e.g., Zira on Windows)
    # for voice in voices:
    #     if "zira" in voice.name.lower():
    #         engine.setProperty('voice', voice.id)
    #         break
    # else:
    #     # If no female voice is found, use the first available voice
    #     engine.setProperty('voice', voices[0].id)

    # Adjust speech rate (lower is slower, higher is faster)
    engine.setProperty('rate', 150)

    # Adjust volume (0.0 to 1.0)
    engine.setProperty('volume', 1.0)


    return engine


def speech_worker():
    """
    Continuously processes the speech queue and speaks messages using a local TTS engine instance.
    """
    global stop_thread
    engine = setup_tts_engine()  # Create a dedicated TTS engine for this thread

    while not stop_thread:
        try:
            # Get the next message from the queue (wait if necessary)
            message = speech_queue.get(timeout=0.1)
            engine.say(message)
            engine.runAndWait()
            time.sleep(2)
            speech_queue.task_done()  # Mark the task as done
        except queue.Empty:
            # If the queue is empty, just loop back and check again
            continue
        except Exception as e:
            print(f"Error in speech worker: {e}")


def speak(message):
    """
    Adds a message to the speech queue to be spoken. If the queue is full,
    the oldest message is removed to make room for the new message.
    """
    if speech_thread is None or not speech_thread.is_alive():
        start_speech_thread()
    try:
        # Add the message to the queue
        speech_queue.put_nowait(message)
    except queue.Full:
        # If the queue is full, remove the oldest message and add the new one
        speech_queue.get_nowait()
        speech_queue.put_nowait(message)


def start_speech_thread():
    """
    Starts the background thread for processing speech messages.
    """
    global speech_thread
    global stop_thread
    stop_thread = False
    speech_thread = threading.Thread(target=speech_worker, daemon=True)
    speech_thread.start()


def stop_speech_thread():
    """
    Signals the speech thread to stop and waits for it to finish.
    """
    global stop_thread
    stop_thread = True
    if speech_thread is not None:
        speech_thread.join()


if __name__ == '__main__':
    # Example usage
    speak("Joystick connected                 .")
    speak("Robot 1 connected                  .")
    speak("Robot 2 disconnected")
    speak("Low battery warning")
    speak("Obstacle detected")
    time.sleep(20)  # Allow time for messages to be spoken
    stop_speech_thread()
