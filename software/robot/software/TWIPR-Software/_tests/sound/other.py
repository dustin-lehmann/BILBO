from TTS.api import TTS

# Load a pre-trained model
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DCA", progress_bar=False, gpu=False)

# Synthesize speech
tts.tts_to_file(text="Hello, this is Coqui TTS!", file_path="output.wav")
