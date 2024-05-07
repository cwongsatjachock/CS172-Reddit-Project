import praw
import json
import config
import prawcore
import time
from praw.models import MoreComments
from bs4 import BeautifulSoup
import requests

reddit = praw.Reddit(
    username=config.username,
    password=config.password,
    client_id=config.client_ID,
    client_secret=config.client_secret,
    user_agent="CS172 Project Phase One"
)

subreddits = ["anime", "technology", "csMajors"]

outputFile = open("output5mb.json", "a")

outputFile.write("[\n")

retry_delay = 90  

for index, subreddit in enumerate(subreddits):
    for _ in range(5):  # Maximum of 5 attempts
        try:
            top = list(reddit.subreddit(subreddit).top(limit=1000))
            new = list(reddit.subreddit(subreddit).new(limit=1000))
            hot = list(reddit.subreddit(subreddit).hot(limit=1000))
            break  
        except prawcore.exceptions.TooManyRequests as e:
            time.sleep(retry_delay)
        except prawcore.exceptions.Forbidden as e:
            time.sleep(retry_delay)

    final = top + new + hot
    final = set(final)
    for i, post in enumerate(final):
        for _ in range(5):  # Maximum of 5 attempts
            try:
                urls_data = []

                if (post.selftext_html != None):
                    soup = BeautifulSoup(post.selftext_html, 'html.parser')
                    for link in soup.find_all('a'):
                        url = link.get('href')
                        try:
                            source_code = requests.get(url)
                            soup2 = BeautifulSoup(source_code.content, 'html.parser')

                            url_data = {
                            "url": url,
                            "title": soup2.title.string if soup2.title else "none"
                            }
                            urls_data.append(url_data)
                        except requests.exceptions.ConnectionError as e:
                            continue
                        except requests.exceptions.MissingSchema as e:
                            continue
                        except requests.exceptions.InvalidSchema as e:
                            continue
                
                comments_data = []

                for comment in post.comments[:10]:
                    if isinstance(comment, MoreComments):
                        continue

                    comment_data = {
                        "author": comment.author.name if comment.author else 'deleted-user',
                        "body": comment.body
                    }

                    comments_data.append(comment_data)
                break 
            except prawcore.exceptions.TooManyRequests as e:
                time.sleep(retry_delay)
            except prawcore.exceptions.Forbidden as e:
                time.sleep(retry_delay)

        post_to_json = {
            "subreddit": subreddit,
            "author": post.author.name if post.author else 'deleted-user',
            "title": post.title,
            "selftext": post.selftext,
            "post ID": post.id,
            "score": post.score,
            "permalink": post.permalink,
            "image url": post.url,
            "comments": comments_data,
            "urls": urls_data
        }

        json.dump(post_to_json, outputFile, indent=6)

        if index < len(subreddits) - 1 or i < len(final) - 1:
            outputFile.write(',\n')

outputFile.write("\n]")

outputFile.close()