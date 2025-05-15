import os
from moviepy.editor import concatenate_videoclips, AudioFileClip
from utils.captionCreate import create_title_card, create_comment_card
from utils.audioGenerator import soundifyPost, combine_audio_segments
from utils.backgroundSelect import get_background_clip
from utils.subtitleRenderer import generate_word_clips

def createVideo(post, body, theme, folder_name):
    try:
        temp_folder = os.path.join("temp", folder_name)
        export_folder = os.path.join("exports", folder_name)
        os.makedirs(temp_folder, exist_ok=True)
        os.makedirs(export_folder, exist_ok=True)

        # Save raw post body to file (optional)
        with open(os.path.join(temp_folder, "post.txt"), "w", encoding="utf-8") as f:
            f.write(body)

        create_title_card(post.title, post.author.name, f"r/{post.subreddit}", theme, temp_folder)

        chunks = body.split(". ")
        for i, chunk in enumerate(chunks):
            if len(chunk.strip()) == 0:
                continue
            create_comment_card(post.author.name, chunk, i + 1, theme, temp_folder)
            soundifyPost(chunk, temp_folder, f"section_{i}")

        print("🔊 Combining audio segments...")
        audio_path = combine_audio_segments(temp_folder)

        print("🎞️ Generating subtitles...")
        subtitle_clips = generate_word_clips(audio_path, temp_folder)

        print("📼 Finalizing video...")
        background = get_background_clip(audio_path, theme)
        final = concatenate_videoclips([background.set_audio(AudioFileClip(audio_path))])
        for clip in subtitle_clips:
            final = final.set_duration(clip.end).fx(lambda gf, t: gf(t).blit(clip.set_start(clip.start)))
        output_path = os.path.join(export_folder, f"{folder_name}.mp4")
        final.write_videofile(output_path, fps=30)

        print(f"\n✅ Video exported: {output_path}\n")

    except Exception as e:
        print(f"❌ Error generating video: {e}")
