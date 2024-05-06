import praw
import json
import config
import prawcore
import time
from praw.models import MoreComments

reddit = praw.Reddit(
    username=config.username,
    password=config.password,
    client_id=config.client_ID,
    client_secret=config.client_secret,
    user_agent="CS172 Project Phase One"
)

subreddits = ["Home", "AskReddit", "NoStupidQuestions", "facepalm", "interestingasfuck", "Damnthatsinteresting", "AmItheAsshole", "mildlyinfuriating", "Piracy", "AITAH", "gaming", "worldnews", "pcmasterrace", "Unexpected", "news", "politics", "wallstreetbets", "todayilearned", "nottheonion", "explainlikeimfive", "OutOfTheLoop", "buildapc", "Steam", "badroommates", "personalfinance", "antiwork", "anime", "manga", "DnD", "technology", "unpopularopinion", "youtube", "legaladvice", "sysadmin", "relationship_advice", "discordapp", "pcgaming", "Games", "ChatGPT", "2007scape", "PiratedGames", "techsupport", "shitposting", "theydidthemath","cyberpunkgame", "OldSchoolCool", "coolguides", "AskMen", "SteamDeck", "college", "rareinsults", "science", "relationship", "csMajors", "ProgrammerHumor", "cscareerquestions", "Python", "cpp", "learnprogramming","leetcode", "computerscience", "funny", "AskReddit", "Music", "movies", "science", "memes", "Showerthoughts", "pics", "Jokes", "videos", "space", "askscience", "DIY", "books", "EarthPorn", "food", "mildlyinteresting", "LifeProTips", "IAmA", "Art", "gadgets", "GetMotivated", "gifs", "sports", "dataisbeautiful", "Documentaries", "Futurology", "UpliftingNews", "photoshopbattles", "tifu", "listentothis", "history", "nosleep", "WritingPrompts", "philosophy", "television", "InternetIsBeautiful", "wholesomememes", "creepy", "NatureIsFuckingLit"]

outputFile = open("output.json", "a")

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
    
        post_to_json = {
            "subreddit": subreddit,
            "author": post.author.name if post.author else 'deleted-user',
            "title": post.title,
            "selftext": post.selftext,
            "post ID": post.id,
            "score": post.score,
            "permalink": post.permalink,
            "image url": post.url,
            "comments": comments_data
        }

        json.dump(post_to_json, outputFile, indent=6)

        if index < len(subreddits) - 1 or i < len(final) - 1:
            outputFile.write(',\n')

outputFile.write("\n]")

outputFile.close()
