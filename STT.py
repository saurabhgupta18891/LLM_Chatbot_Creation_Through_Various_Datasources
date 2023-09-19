import io
import os
import pyaudio
import wave
from google.cloud import speech_v1p1beta1 as speech
from google.oauth2 import service_account

# Replace with the path to your service account key JSON file
service_account_key_path = r"C:\Users\Saurabh.Gupta\PycharmProjects\pythonProject1\my-project1-391005-c4b99a6fd48e.json"
# Set the project ID for Google Cloud
project_id = "my-project1-391005"

# Authenticate using the service account key
credentials = service_account.Credentials.from_service_account_file(service_account_key_path)
client = speech.SpeechClient(credentials=credentials)

# Set your Google Cloud credentials
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/credentials.json"

# Initialize the Speech-to-Text client
#client = speech.SpeechClient()


def record_audio(filename, duration=20):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Recording...")
    frames = []

    for _ in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Recording done.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


def transcribe_audio(filename):
    with io.open(filename, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="hi-IN" ,   #"en-US",
        model="default"
    )

    response = client.recognize(config=config, audio=audio)
    transcript = ""

    for result in response.results:
        transcript += result.alternatives[0].transcript

    return transcript


if __name__ == "__main__":
    audio_filename = "output.wav"
    record_audio(audio_filename)
    transcript = transcribe_audio(audio_filename)
    print("Transcript:", transcript)
