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

outputFile = open("output.json", "w")

outputFile.write("[\n")

for index, subreddit in enumerate(subreddits):
    top = list(reddit.subreddit(subreddit).top(limit=1000))
    new = list(reddit.subreddit(subreddit).new(limit=1000))
    rising = list(reddit.subreddit(subreddit).rising(limit=1000))
    hot = list(reddit.subreddit(subreddit).hot(limit=1000))
    final = top + new + rising + hot
    final = set(final)
    print(subreddit)
    for i, post in enumerate(final):
        post.comments.replace_more(limit=0)
        comments_data = [
            {
                "author": comment.author.name if comment.author else 'deleted-user',
                "body": comment.body
            }
            for comment in post.comments[:100]
        ]
        print(post)
        post_to_json = {
            "subreddit": subreddit,
            "author": post.author.name if post.author else 'deleted-user',
            "title": post.title,
            "url": post.url,
            "selftext": post.selftext,
            "post ID": post.id,
            "score": post.score,
            "permalink": post.permalink,
            "image url": post.url,
            "comments": comments_data
        }

        json.dump(post_to_json, outputFile, indent=6)

        if index < len(subreddits) - 1 or i < len(top) - 1:
            outputFile.write(',\n')

outputFile.write("\n]")

outputFile.close()
