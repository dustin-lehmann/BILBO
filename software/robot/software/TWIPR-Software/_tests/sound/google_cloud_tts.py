from google.cloud import texttospeech

def speak_google_cloud(text, lang="en-US", voice_name="en-US-Wavenet-D"):
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=lang,
        name=voice_name
    )

    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

    # Save the response to an audio file
    with open("output.mp3", "wb") as out:
        out.write(response.audio_content)
        print('Audio content written to "output.mp3"')

# Example usage
speak_google_cloud("Hello, this is Google Cloud Text-to-Speech!")
