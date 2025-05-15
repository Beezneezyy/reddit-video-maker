import os
import math
import numpy as np
from pydub import AudioSegment
import subprocess
from moviepy.editor import TextClip, CompositeVideoClip

FONT_PATH = "assets/fonts/RedditSans-Bold.ttf"

def extract_word_timestamps(audio_path, output_path):
    from whisper_timestamped import load_model, transcribe_timestamped
    model = load_model("tiny")
    audio = AudioSegment.from_file(audio_path)
    audio.export("temp.wav", format="wav")
    result = transcribe_timestamped(model, "temp.wav")
    words = []
    for segment in result["segments"]:
        for w in segment["words"]:
            words.append(w)
    return words

def style_word(word, theme):
    color = "white"
    stroke = "black"
    return dict(font=FONT_PATH, fontsize=60, color=color, stroke_color=stroke, stroke_width=2)

def generate_word_clips(audio_path, folder_path):
    words = extract_word_timestamps(audio_path, folder_path)
    clips = []

    for word in words:
        text = word['text'].strip()
        if not text or word['end'] - word['start'] <= 0:
            continue

        style = style_word(text, "dark")
        clip = (
            TextClip(text, font=style["font"], fontsize=style["fontsize"],
                     color=style["color"], stroke_color=style["stroke_color"],
                     stroke_width=style["stroke_width"])
            .set_start(word['start'])
            .set_duration(word['end'] - word['start'])
            .set_position("center")
        )
        clips.append(clip)

    return clips
