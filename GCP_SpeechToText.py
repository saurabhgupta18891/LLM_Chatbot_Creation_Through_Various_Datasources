from google.cloud import speech_v1p1beta1 as speech
from google.oauth2 import service_account
from pydub import AudioSegment
import io
from google.cloud.speech_v1p1beta1 import types

# Replace with the path to your service account key JSON file
service_account_key_path = r"C:\Users\Saurabh.Gupta\PycharmProjects\pythonProject1\my-project1-391005-c4b99a6fd48e.json"
# Set the project ID for Google Cloud
project_id = "my-project1-391005"

# Authenticate using the service account key
credentials = service_account.Credentials.from_service_account_file(service_account_key_path)
#client = speech.SpeechClient(credentials=credentials)

def convert_audio_to_mono(input_audio_path, output_audio_path):
    # Load the audio file
    audio = AudioSegment.from_wav(input_audio_path)

    # Ensure that the audio is in mono (single-channel)
    audio = audio.set_channels(1)

    # Export the mono audio to a new file
    audio.export(output_audio_path, format="wav")

def transcribe_mono_audio(audio_file_path):
    # Initialize the Google Cloud Speech-to-Text client
    client = speech.SpeechClient(credentials=credentials)

    # Read the mono audio file
    with io.open(audio_file_path, 'rb') as audio_file:
        content = audio_file.read()

    # Configure the audio settings
    # config = {
    #     "language_code": "en-US",  # Adjust this based on the language of the audio
    # }
    # audio = {"content": content}
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code="en-US",  # "en-US",
        model="default")

    # Perform the transcription
    response = client.recognize(config=config, audio=audio)

    # Process and return the transcribed text
    transcribed_text = ""
    for result in response.results:
        transcribed_text += result.alternatives[0].transcript

    return transcribed_text

if __name__ == "__main__":
    input_audio_file_path = "harvard.wav"  # Replace with the path to your stereo audio file
    mono_audio_file_path = "mono_audio.wav"  # Path to save the mono audio file
    convert_audio_to_mono(input_audio_file_path, mono_audio_file_path)

    transcript = transcribe_mono_audio(mono_audio_file_path)
    print("Transcript:")
    print(transcript)



