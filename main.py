# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "elevenlabs",
#   "pydub",
#   "python-dotenv",
#   "audioop-lts",
# ]
# ///

import re
import sys
import os
import io
from elevenlabs import ElevenLabs, play
from pydub import AudioSegment
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("ELEVENLABS_API_KEY")
if not API_KEY:
    print("Please set the ELEVENLABS_API_KEY environment variable in a .env file.")
    sys.exit(1)

# Add speakers here (to find the voice ID, go to Voices -> Library -> View -> ID), also ensure to "Add Voice" in the 
# web application or else it will not find the voices.
SPEAKER_VOICE_MAP = {
    "Aria": "9BWtsMINqrJLrRacOk9x",
    "Roger": "CwhRBWXzGAHq8TQ4Fs17",
    "Lily": "pFZP5JQG7iQjIQuC4Bku",
}

MODEL_ID = "eleven_multilingual_v2"
OUTPUT_FORMAT = "mp3_44100_128"

def parse_script(text):
    pattern = r"\[([^\]]+)\]\s*(.*?)(?=\n\[|$)"
    segments = re.findall(pattern, text, re.DOTALL)
    return [(speaker.strip(), dialogue.strip()) for speaker, dialogue in segments]

def generate_audio_segment(text, voice_id, previous_text="", next_text=""):
    audio_generator = client.text_to_speech.convert(
        text=text,
        voice_id=voice_id,
        model_id=MODEL_ID,
        output_format=OUTPUT_FORMAT,
        previous_text=previous_text,
        next_text=next_text
    )
    audio_bytes = b"".join(audio_generator)
    return AudioSegment.from_file(io.BytesIO(audio_bytes), format="mp3")

def main(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    segments = parse_script(content)
    if not segments:
        print("No dialogue segments found. Ensure your file is annotated with [Speaker].")
        sys.exit(1)

    global client
    client = ElevenLabs(api_key=API_KEY)

    audio_segments = []
    for i, (speaker, dialogue) in enumerate(segments):
        if speaker not in SPEAKER_VOICE_MAP:
            print(f"Warning: No voice mapping for speaker '{speaker}'. Skipping this segment.")
            continue
        voice_id = SPEAKER_VOICE_MAP[speaker]
        previous_text = segments[i-1][1] if i > 0 else ""
        next_text = segments[i+1][1] if i < len(segments)-1 else ""
        print(f"Generating audio for {speaker}: {dialogue[:100]}...")
        segment_audio = generate_audio_segment(dialogue, voice_id, previous_text, next_text)
        audio_segments.append(segment_audio)

    if not audio_segments:
        print("No audio segments generated. Exiting.")
        sys.exit(1)

    # Insert a pause between segments.
    pause = AudioSegment.silent(duration=0)
    combined_audio = audio_segments[0]
    for seg in audio_segments[1:]:
        combined_audio += pause + seg

    combined_audio.export(output_file, format="mp3")
    print(f"Final audio saved to '{output_file}'.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: uv run main.py <input_text_file> <output_audio.mp3>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
