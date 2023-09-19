import boto3
from langdetect import detect
import json

# Initialize AWS Transcribe client
def transcribe_audio_to_text(audio_file_path, output_bucket):
    aws_access_key_id = 'AKIAV6B6R4UDOUPFE3II'
    aws_secret_access_key = '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'
    region_name = 'ap-south-1'
    transcribe = boto3.client('transcribe', region_name=region_name,
                                  aws_access_key_id=aws_access_key_id,
                                  aws_secret_access_key=aws_secret_access_key)
    job_name = 'multi_audio_to_text_job1'
    output_bucket="dev-amp-videos"
    audio_file_path=r"C:\Users\Saurabh.Gupta\PycharmProjects\pythonProject1\Pre-Summit(G20 presidency).mp4"
    # Specify the audio file and language detection threshold
    s3 = boto3.client('s3', region_name=region_name,
                          aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key)

        # Upload the .wav audio file to the S3 bucket
    s3.upload_file(audio_file_path, output_bucket, job_name + '.mp4')
    audio_file_uri = f's3://{output_bucket}/{job_name}.mp4'

    language_detection_threshold = 0.8  # Adjust as needed

    # Transcribe the audio
    # response = transcribe.start_transcription_job(
    #     TranscriptionJobName=job_name,
    #     Media={'MediaFileUri': audio_file_uri},
    #     MediaFormat='mp4',
    #     LanguageCode='auto'  # Automatically detect the language
    # )
    response=transcribe.start_transcription_job(
        TranscriptionJobName = job_name,
        Media = {
            'MediaFileUri': audio_file_uri
        },
        OutputBucketName = output_bucket,
        MediaFormat = 'mp4',
        IdentifyMultipleLanguages = True, # (or IdentifyMultipleLanguages = True),
        LanguageOptions = [
            'en-US', 'hi-IN'
        ]
    )
    # Wait for the transcription job to complete
    transcription_job_name = response['TranscriptionJob']['TranscriptionJobName']
    # transcribe.get_waiter('transcription_job_completed').wait(TranscriptionJobName=transcription_job_name)

    # Get the transcription results
    transcription_response = transcribe.get_transcription_job(TranscriptionJobName=transcription_job_name)
    transcript_file_name = f'{job_name}.json'

    # Specify the local file path where you want to save the downloaded JSON file
    local_file_path = r'C:\Users\Saurabh.Gupta\PycharmProjects\pythonProject1\Transcripted_data\transcrited_file_g20.json'

    # Download the JSON file from S3
    s3.download_file(output_bucket, transcript_file_name, local_file_path)

    print(f"Downloaded '{transcript_file_name}' from S3 to '{local_file_path}'.")

    # Parse the JSON data
    with open(local_file_path, 'r') as json_file:
        transcript_data = json.load(json_file)

    # Extract the transcript text
    transcript_text = transcript_data['results']['transcripts'][0]['transcript']


    # Detect the language of the transcription text
    detected_language = detect(transcript_text)

    # Print the detected language and the transcription text
    # print('Detected language:', detected_language)
    # print('Transcription text:', transcript_text)

transcript = transcribe_audio_to_text(
    r'C:\Users\Saurabh.Gupta\PycharmProjects\pythonProject1\Pre-Summit(G20 presidency).mp4', 'dev-amp-videos')
print("Transcript Text:")
print(transcript)



# import time
# import boto3
# transcribe = boto3.client('transcribe', 'us-west-2')
# job_name = "my-first-transcription-job"
# job_uri = "s3://DOC-EXAMPLE-BUCKET/my-input-files/my-media-file.flac"
# transcribe.start_transcription_job(
#     TranscriptionJobName = job_name,
#     Media = {
#         'MediaFileUri': job_uri
#     },
#     OutputBucketName = 'DOC-EXAMPLE-BUCKET',
#     OutputKey = 'my-output-files/',
#     MediaFormat = 'flac',
#     IdentifyLanguage = True, # (or IdentifyMultipleLanguages = True),
#     LanguageOptions = [
#         'en-US', 'hi-IN'
#     ]
# )
#
# while True:
#     status = transcribe.get_transcription_job(TranscriptionJobName = job_name)
#     if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
#         break
#     print("Not ready yet...")
#     time.sleep(5)
# print(status)
