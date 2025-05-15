import praw
import json
import os

try:
    with open("client_details.json", "r") as file:
        data = json.load(file)
except:
    print("[ERROR]: Cannot find file client_details.json")
    data = {}

reddit = praw.Reddit(
    client_id=data.get("client_id", ""),
    client_secret=data.get("client_secret", ""),
    user_agent=data.get("user_agent", "reddit-video-bot")
)


def get_used_ids(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return set(json.load(f))
    return set()


def save_used_ids(path, ids):
    with open(path, "w") as f:
        json.dump(list(ids), f)


def get_posts(subreddit, count, span, used_ids):
    subreddit = reddit.subreddit(subreddit)
    posts = []
    for submission in subreddit.top(span, limit=30):
        if submission.id in used_ids:
            continue
        if "r/" not in submission.title.lower() and "reddit" not in submission.title.lower():
            posts.append(submission)
        if len(posts) >= count:
            break
    return posts


def scrapeText(subreddit, count, span, used_ids_path, max_length):
    used_ids = get_used_ids(used_ids_path)
    posts = get_posts(subreddit, count, span, used_ids)
    postText = []

    for post in posts:
        if post.selftext and len(post.selftext.split()) < 1000:
            postText.append([post, post.selftext])
            used_ids.add(post.id)

    save_used_ids(used_ids_path, used_ids)
    return postText


def scrapeComments(subreddit, count, span, used_ids_path, max_length):
    used_ids = get_used_ids(used_ids_path)
    posts = get_posts(subreddit, count, span, used_ids)
    all_comments = []

    for post in posts:
        post.comment_sort = "best"
        comments = []
        try:
            post.comments.replace_more(limit=0)
        except:
            continue

        for top_comment in post.comments:
            if "http" in top_comment.body:
                continue
            comments.append(top_comment)
            if len(comments) >= 6:
                break

        if comments:
            all_comments.append([post] + comments)
            used_ids.add(post.id)

    save_used_ids(used_ids_path, used_ids)
    return all_comments
