import boto3
import json

def transcribe_audio_to_text(audio_file_path, output_bucket, target_language='en-US'):
    # Initialize the S3 client
    s3 = boto3.client('s3')

    # Specify the job name (a unique name for this transcription job)
    job_name = 'audio_to_text_job1'

    try:
        # Upload the audio file to the S3 bucket
        s3.upload_file(audio_file_path, output_bucket, job_name + '.mp4')

        # Initialize the AWS Transcribe client
        transcribe = boto3.client('transcribe')

        # Start the transcription job with the specified language
        response = transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            LanguageCode=target_language,
            MediaFormat='mp4',
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
        local_file_path = f'transcripted_file_{job_name}.json'

        # Download the JSON file from S3
        s3.download_file(output_bucket, transcript_file_name, local_file_path)

        print(f"Downloaded '{transcript_file_name}' from S3 to '{local_file_path}'.")

        # Parse the JSON data
        with open(local_file_path, 'r') as json_file:
            transcript_data = json.load(json_file)

        # Extract the transcript text
        transcript_text = transcript_data['results']['transcripts'][0]['transcript']

        # Save the transcript to a text file (optional)
        with open('transcript.txt', 'w') as txt_file:
            txt_file.write(transcript_text)

        return transcript_text

    except Exception as e:
        print("An error occurred:", str(e))

# Example usage:
# Replace 'your_audio_file.wav' and 'your_s3_bucket' with your audio file path and S3 bucket name.
# Specify the target language (e.g., 'en-US', 'es-US', 'fr-FR', etc.)
transcript = transcribe_audio_to_text('your_audio_file.wav', 'your_s3_bucket', target_language='en-US')
print("Transcript Text:")
print(transcript)
