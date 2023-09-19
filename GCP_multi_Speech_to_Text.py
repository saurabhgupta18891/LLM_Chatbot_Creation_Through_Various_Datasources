from google.cloud import speech_v1p1beta1 as speech
from google.oauth2 import service_account
from google.cloud import storage
from pydub import AudioSegment
import io
from moviepy.editor import AudioFileClip

# Function to extract audio from an .mp4 audio file and save it as WAV
def extract_audio(input_audio_mp4_path, output_audio_path):
    audio = AudioFileClip(input_audio_mp4_path)
    audio.write_audiofile(output_audio_path)

# Replace with the path to your service account key JSON file
service_account_key_path = r"C:\Users\Saurabh.Gupta\PycharmProjects\pythonProject1\my-project1-391005-c4b99a6fd48e.json"


# Set the project ID for Google Cloud
project_id = "my-project1-391005"

# Set the bucket name
bucket_name = "training_data_palm2"
#https://console.cloud.google.com/storage/browser/training_data_palm2;tab=objects?forceOnBucketsSortingFiltering=false&project=my-project1-391005

# Initialize Google Cloud Storage client
storage_client = storage.Client(credentials=service_account.Credentials.from_service_account_file(service_account_key_path))

# Authenticate using the service account key
credentials = service_account.Credentials.from_service_account_file(service_account_key_path)

def upload_audio_to_bucket(audio_file_path, bucket_name, destination_blob_name):
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(audio_file_path)
    print(f"Audio file uploaded to bucket: gs://{bucket_name}/{destination_blob_name}")

def transcribe_audio_from_bucket(bucket_name, audio_blob_name):
    # Initialize the Google Cloud Speech-to-Text client
    client = speech.SpeechClient(credentials=credentials)

    # Configure the audio settings
    audio = {"uri": f"gs://{bucket_name}/{audio_blob_name}"}
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code="hi-IN",
        sample_rate_hertz=44100,
        audio_channel_count=2,
        alternative_language_codes=["en-US","en-IN"],
        model="default")

    # Perform the transcription
    #response = client.recognize(config=config, audio=audio)
    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result()

    # Process and return the transcribed text
    # transcribed_text = ""
    # for result in response.results:
    #     for alternative in result.alternatives:
    #         transcribed_text += alternative.transcript + "\n"
    #
    # # Save the transcript to a text file
    # with open('transcript_news_gcp1.txt', 'w',encoding='utf-8') as txt_file:
    #     txt_file.write(transcribed_text)
    #
    # return transcribed_text
    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        print("-" * 20)
        print(f"First alternative of result {i}: {alternative}")
        print(f"Transcript: {alternative.transcript}")

    return response.results

    # transcript_builder = []
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    # for result in response.results:
    #     # The first alternative is the most likely one for this portion.
    #     transcript_builder.append(f"\nTranscript: {result.alternatives[0].transcript}")
    #     transcript_builder.append(f"\nConfidence: {result.alternatives[0].confidence}")
    #
    # transcript = "".join(transcript_builder)
    # #print(transcript)
    #
    # return transcript

if __name__ == "__main__":
    #input_audio_mp4_file_path = r"C:\Users\Saurabh.Gupta\PycharmProjects\pythonProject1\Pre-Summit(G20 presidency).mp4"
    input_audio_mp4_file_path= r"C:\Users\Saurabh.Gupta\PycharmProjects\pythonProject1\news.mp3"# Replace with the path to your .mp4 audio file
    #output_audio_file_path = "Pre-Summit(G20 presidency).wav"  # Output audio file in WAV format
    output_audio_file_path="news.wav"
    # Extract audio from the .mp4 audio file and save it as WAV
    extract_audio(input_audio_mp4_file_path, output_audio_file_path)

    # Upload the audio file to the bucket
    audio_blob_name = "news.wav"  # Name to use for the audio file in the bucket
    upload_audio_to_bucket(output_audio_file_path, bucket_name, audio_blob_name)

    # Transcribe the audio from the bucket
    transcript = transcribe_audio_from_bucket(bucket_name, audio_blob_name)
    print("Transcript:")
    print(transcript)
