import os
from gtts import gTTS
from pydub import AudioSegment

def soundifyPost(text, temp_path, filename, folder):
    output_path = os.path.join(folder, f"{filename}.mp3")
    try:
        tts = gTTS(text)
        tts.save(output_path)
    except Exception as e:
        print(f"⚠️ Skipping corrupted segment {filename}.mp3: {e}")

def combine_audio_segments(folder_path):
    combined = AudioSegment.empty()
    files = sorted(f for f in os.listdir(folder_path) if f.endswith(".mp3"))
    
    if not files:
        raise Exception("No MP3 segments found.")

    for file in files:
        path = os.path.join(folder_path, file)
        try:
            audio = AudioSegment.from_file(path)
            combined += audio
        except Exception as e:
            print(f"⚠️ Skipping {file}: {e}")

    output_path = os.path.join(folder_path, "combined.mp3")
    combined.export(output_path, format="mp3")
