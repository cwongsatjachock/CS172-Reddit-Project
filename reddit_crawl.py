import praw
import json
import config

print(config.username)

reddit = praw.Reddit(
    username = config.username,
    password = config.password,
    client_id = config.client_ID,
    client_secret = config.client_secret,
    user_agent = "CS172 Project Phase One"
)

top = reddit.subreddit("csMajors").top(limit=500)
for post in top:
    print(post.selftext)
    print(post.title)
    print(post.id)
    print(post.score)
    print(post.url)
    print(post.permalink)

