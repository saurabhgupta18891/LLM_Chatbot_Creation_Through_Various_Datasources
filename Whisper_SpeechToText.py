# # Note: you need to be using OpenAI Python v0.27.0 for the code below to work
# import openai
# from pydub import AudioSegment
# import os
# from dotenv import load_dotenv
#
# load_dotenv()
#
# openai.api_key = os.environ.get('OPENAI_API_KEY', None)
# from pathlib import Path
# mp4_path = Path(r"C:\Users\Saurabh.Gupta\PycharmProjects\pythonProject1\Pre-Summit(G20 presidency).mp4")
# mp4_audio = AudioSegment.from_file(mp4_path)
#
# song = AudioSegment.from_mp3(r"C:\Users\Saurabh.Gupta\PycharmProjects\pythonProject1\Pre-Summit(G20 presidency).mp4")
# #
# # # PyDub handles time in milliseconds
# # ten_minutes = 10 * 60 * 1000
# #
# # first_10_minutes = song[:ten_minutes]
# #
# # first_10_minutes.export("good_morning_10.mp3", format="mp3")
#
# # audio_file= open(r"C:\Users\Saurabh.Gupta\PycharmProjects\pythonProject1\Pre-Summit(G20 presidency).mp4", "rb")
# #
# # transcript = openai.Audio.transcribe("whisper-1", audio_file)
# #
# # print(transcript["text"])







import openai
from pydub import AudioSegment
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.environ.get('OPENAI_API_KEY', None)

# Input audio file path
#input_audio_path = r"C:\Users\Saurabh.Gupta\PycharmProjects\pythonProject1\Pre-Summit(G20 presidency).mp4"
#input_audio_path=r"C:\Users\Saurabh.Gupta\PycharmProjects\pythonProject1\G20.mp3"

from pathlib import Path
mp4_path = Path(r"C:\Users\Saurabh.Gupta\Desktop\Pre-Summit(G20 presidency).mp4")
song = AudioSegment.from_file(mp4_path)
# Output transcript path
output_transcript_path = "transcript_g20_presumm_whisp.txt"

# Load the audio file
#song = AudioSegment.from_file(input_audio_path, format="mp4")

# Set the maximum segment size (in milliseconds)
max_segment_size = 25 * 60 * 1000  # 25 minutes

# Initialize variables for segment start and end
segment_start = 0

# Initialize an empty list to store individual segment transcripts
segment_transcripts = []

while segment_start < len(song):
    # Calculate segment end based on the maximum segment size
    segment_end = min(segment_start + max_segment_size, len(song))

    # Extract the segment
    segment = song[segment_start:segment_end]

    # Export the segment to a temporary audio file
    temp_segment_path = "temp_segment.mp4"
    segment.export(temp_segment_path, format="mp4")

    # Open the temporary audio file
    audio_file = open(temp_segment_path, "rb")

    # Transcribe the segment using the Whisper API
    transcript = openai.Audio.transcribe("whisper-1", audio_file)

    # Append the segment transcript to the list
    segment_transcripts.append(transcript["text"])

    # Move the segment start to the next segment
    segment_start = segment_end

    # Close and remove the temporary audio file
    audio_file.close()
    os.remove(temp_segment_path)

# Combine all segment transcripts into a single transcript
full_transcript = "\n".join(segment_transcripts)

# Save the full transcript to a file
with open(output_transcript_path, "w") as transcript_file:
    transcript_file.write(full_transcript)

# Print the full transcript
print(full_transcript)

