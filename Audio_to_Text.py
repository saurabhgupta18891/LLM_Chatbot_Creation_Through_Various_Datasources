import boto3
import json

def transcribe_audio_to_text(audio_file_path, output_bucket):
    # Replace these with your AWS credentials and desired region
    aws_access_key_id = 'AKIAV6B6R4UDOUPFE3II'
    aws_secret_access_key = '3TcCLuL0LYvX8WN++Wy0tF32rfBArlSzhqJj1Mmk'
    region_name = 'ap-south-1'
    # Change to your desired AWS region

    # Initialize the S3 client
    s3 = boto3.client('s3', region_name=region_name,
                      aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key)

    # Specify the job name (a unique name for this transcription job)
    job_name = 'audio_to_text_job1'

    # Upload the .wav audio file to the S3 bucket
    s3.upload_file(audio_file_path, output_bucket, job_name + '.mp4')

    # Initialize the AWS Transcribe client
    transcribe = boto3.client('transcribe', region_name=region_name,
                              aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_secret_access_key)

    # Start the transcription job
    response = transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        LanguageCode='en-US',  # Change the language code if necessary
        MediaFormat='mp4',  # Change the format if your audio is different
        Media={
            'MediaFileUri': f's3://{output_bucket}/{job_name}.mp4'
        },
        OutputBucketName=output_bucket
    )

    # Check the status of the transcription job
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break

    print("Transcription job status:", status['TranscriptionJob']['TranscriptionJobStatus'])

    # If the job is completed successfully, fetch the transcript
    transcript_url = None
    if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        transcript_url = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
        print("Transcript URL:", transcript_url)
    else:
        print("Transcription job failed.")

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

    # Save the transcript to a text file
    # with open('transcript_g20.txt', 'w') as txt_file:
    #     txt_file.write(transcript_text)

    return transcript_text

# Example usage:
# Replace 'your_audio_file.wav' and 'your_s3_bucket' with your audio file path and S3 bucket name.
transcript = transcribe_audio_to_text(
    r'C:\Users\Saurabh.Gupta\PycharmProjects\pythonProject1\Pre-Summit(G20 presidency).mp4', 'dev-amp-videos')
print("Transcript Text:")
print(transcript)

# # # You can download the transcript from the URL or process it further as needed
# # # Define the local file path where you want to save the transcript
# # local_transcript_file = 'transcript.txt'
# #
# # # Make an HTTP GET request to the transcript URL
# # response = requests.get(transcript_url)
# #
# # # Check if the request was successful (status code 200)
# # if response.status_code == 200:
# #     # Save the transcript to a local file
# #     with open(local_transcript_file, 'wb') as file:
# #         file.write(response.content)
# #     print(f"Transcript downloaded and saved to '{local_transcript_file}'.")
# # else:
# #     print("Failed to download the transcript. HTTP Status Code:", response.status_code)





