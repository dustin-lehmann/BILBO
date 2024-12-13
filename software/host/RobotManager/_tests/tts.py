import asyncio
import threading
import queue
import os
import uuid
import edge_tts
import pygame


class TTSManager:
    def __init__(self, voice="en-GB-RyanNeural", output_dir="tts_output"):
        """
        Initialize the TTS Manager.
        :param voice: Default voice for TTS.
        :param output_dir: Directory to save generated audio files.
        """
        self.voice = voice
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        # Queues for text generation and playback
        self.generation_queue = queue.Queue()
        self.playback_queue = queue.Queue()

        # Background thread
        self.running = True
        self.thread = threading.Thread(target=self._process_queues)
        self.thread.daemon = True
        self.thread.start()

        # Initialize pygame mixer for audio playback
        pygame.mixer.init()

    def speak(self, text):
        """
        Add a text to the generation queue for TTS.
        :param text: Text to generate and play.
        """
        self.generation_queue.put(text)

    def stop(self):
        """
        Stop the TTS Manager and terminate the background thread.
        """
        self.running = False
        self.thread.join()
        pygame.mixer.quit()

    def _generate_speech(self, text):
        """
        Generate speech for a given text using edge-tts.
        :param text: Text to generate speech for.
        :return: Path to the generated audio file.
        """
        filename = f"{uuid.uuid4()}.mp3"
        filepath = os.path.join(self.output_dir, filename)
        asyncio.run(self._generate_tts_async(text, filepath))
        return filepath

    async def _generate_tts_async(self, text, output_file):
        """
        Asynchronous TTS generation using edge-tts.
        :param text: Text to generate.
        :param output_file: Path to save the generated audio file.
        """
        communicate = edge_tts.Communicate(text, voice=self.voice)
        await communicate.save(output_file)

    def _process_queues(self):
        """
        Process the generation and playback queues in a background thread.
        """
        while self.running:
            try:
                # Check for text to generate
                if not self.generation_queue.empty():
                    text = self.generation_queue.get()
                    print(f"Generating speech for: {text}")
                    audio_file = self._generate_speech(text)
                    self.playback_queue.put(audio_file)

                # Check for audio to play
                if not self.playback_queue.empty():
                    audio_file = self.playback_queue.get()
                    self._play_audio(audio_file)

            except Exception as e:
                print(f"Error in processing queues: {e}")

    def _play_audio(self, file_path):
        """
        Play the given audio file using pygame.
        :param file_path: Path to the audio file.
        """
        print(f"Playing: {file_path}")
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():  # Wait until playback finishes
            pygame.time.Clock().tick(10)


# Example usage
if __name__ == "__main__":
    tts_manager = TTSManager()

    try:
        tts_manager.speak("Robot 1 connected")
        tts_manager.speak("Bilbo 1 disconnected")
        tts_manager.speak("Joystick 1 connected")

        # Keep the main thread alive while the background thread works
        while tts_manager.generation_queue.qsize() > 0 or tts_manager.playback_queue.qsize() > 0:
            pygame.time.Clock().tick(10)

    except KeyboardInterrupt:
        print("\nExiting...")

    finally:
        tts_manager.stop()
