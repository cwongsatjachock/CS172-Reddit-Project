import praw
import json
import config

reddit = praw.Reddit(
    username=config.username,
    password=config.password,
    client_id=config.client_ID,
    client_secret=config.client_secret,
    user_agent="CS172 Project Phase One"
)

subreddits = ["Home", "AskReddit", "NoStupidQuestions", "BaldursGate3", "facepalm", "interestingasfuck", "Damnthatsinteresting", "LivestreamFail", "pics", "Palworld", "AmItheAsshole", "mildlyinfuriating", "Piracy", "PeterExplainsTheJoke", "funny", "AITAH", "movies", "Helldivers", "gaming", "worldnews", "leagueoflegends", "pcmasterrace", "Unexpected", "news", "politics", "wallstreetbets", "todayilearned", "nottheonion", "memes", "PublicFreakout", "Wellthatsucks", "explainlikeimfive", "OutOfTheLoop", "OnePiece", "BlackPeopleTwitter", "buildapc", "HonkaiStarRail", "SipsTea", "Minecraft", "mildlyinteresting", "nfl", "BeAmazed", "DIY", "nba", "MapPorn", "Steam", "Overwatch", "Genshin_Impact", "classicwow", "soccer", "Eldenring", "badroommates", "personalfinance", "antiwork", "anime", "wow", "DnD", "technology", "WhitePeopleTwitter", "EscapefromTarkov", "unpopularopinion", "popculturechat", "videos", "BestofRedditorUpdates", "youtube", "legaladvice", "ffxiv", "sysadmin", "MadeMeSmile", "CombatFootage", "relationship_advice", "discordapp", "pcgaming", "Games", "ChatGPT", "GlobalOffensive", "2007scape", "formula1", "CuratedTumblr", "Gamingcirclejerk", "TikTokCringe", "PiratedGames", "techsupport", "shitposting", "theydidthemath", "malelivingspace", "WTF", "cyberpunkgame", "OldSchoolCool", "coolguides", "AskMen", "dankmemes", "feedthebeast", "Warframe", "UkraineWarVideoReport", "SteamDeck", "college", "manga", "CrazyFuckingVideos", "rareinsults"]
data = []

for subreddit in subreddits:
    top = list(reddit.subreddit(subreddit).top(limit=1000))
    new = list(reddit.subreddit(subreddit).new(limit=1000))
    final = top + new
    set(final)
    for post in final:
        post.comments.replace_more(limit=0)
        comments_data = [
            {
                "author": comment.author.name if comment.author else 'deleted-user',
                "body": comment.body
            }
            for comment in post.comments[:1000]
        ]

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

        data.append(post_to_json)

with open("output.json", "w") as outputFile:
    json.dump(data, outputFile, indent=4)
