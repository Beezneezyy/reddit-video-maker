import os
from utils.redditScraper import scrapeText
from utils.videoCreate import createVideo

def long_form():
    video_type = input("Enter video type (lf/ar): ").strip()
    count = int(input("Enter video count (1-10): ").strip())
    span = input("Enter time range (day/week): ").strip()
    theme = input("Choose theme (dark/light): ").strip()
    max_length = int(input("Enter max video length in seconds: ").strip())
    subreddit = input("What subreddit: ").strip()

    print(f"\n🔄 Starting video generation for r/{subreddit}...\n")

    used_ids_path = "used_ids.json"
    posts = scrapeText(subreddit, count, span, used_ids_path, max_length)

    for post, body in posts:
        try:
            print(f"🧠 Processing post by u/{post.author.name}: {post.title[:60]}...")
            safe_post_id = post.id
            createVideo(post, body, theme, safe_post_id)
        except Exception as e:
            print(f"❌ Error generating video: {e}")
            continue

if __name__ == "__main__":
    long_form()
