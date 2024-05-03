# REMINDER: Reddit search engine should:
#               * Show relevant reddit posts given a search query (give weights to upvotes, titles, tags, etc)
#               * Have the ability to search by user name, or on "trending", "new", etc

import praw
import json
import config
import time

def retrieveData(postType):
    for i, post in enumerate(postType):
        # Tracks the collected post/progress of data collection
        # collectedPosts = collectedPosts + 1
        # print(collectedPosts, "/" ,expectedPosts)

        # Retrieval of basic post information
        selftext = post.selftext
        authorname = post.author.name if post.author else 'deleted-user'
        title = post.title
        postID = post.id
        score = post.score
        ratio = post.upvote_ratio
        imgurl = post.url
        permalink = post.permalink

        # Grabs comments and its data
        comments_data = []
        for comment in post.comments[:5]:
            # Ignore empty comments
            if not comment.body.strip():
                continue

            comment_author = comment.author.name if comment.author else 'deleted-user'
            comment_body = comment.body

            comment_data = {
                "author": comment_author,
                "body": comment_body
            }

            comments_data.append(comment_data)
        
        post_to_json = {
            "subreddit": subreddit,
            "author": authorname,
            "title": title,
            "selftext": selftext,
            "post ID": postID,
            "score": score,
            "upvote ratio": ratio,
            "permalink": permalink,
            "image url": imgurl,
            "comments": comments_data
        }

        json.dump(post_to_json, outputFile, indent=6)

        if i < len(postType) - 1:
            outputFile.write(',\n')

# Initial login - references config, which contains an individual reddit login and the reddit dev app info, like the client id and secret
reddit = praw.Reddit(
    username = config.username,
    password = config.password,
    client_id = config.client_ID,
    client_secret = config.client_secret,
    user_agent = "CS172 Project Phase One"
)

# Open the file
outputFile = open("output.json", "w")

# FOR TESTING PURPOSES - NOT SURE IF WE SHOULD HAVE THIS IN FINAL IMPLEMENTATION
# Clears the file
outputFile.write("")

# Correctly formats the JSON file with brackets
outputFile.write("[\n")

# Provide a list of subreddits to iterate through and loop through each subreddit
subreddits = ["AskReddit", "worldnews", "mildlyinteresting", "explainlikeimfive", "LifeProTips", "lifehacks"]

collectedPosts = 0
numSubreddits = len(subreddits)
numPosts = 10
expectedPosts = numPosts * numSubreddits

for subreddit_index, subreddit in enumerate(subreddits):
    top = list(reddit.subreddit(subreddit).top(limit = numPosts))
    new = list(reddit.subreddit(subreddit).new(limit = numPosts))
    hot = list(reddit.subreddit(subreddit).hot(limit = numPosts))

    retrieveData(top)
    outputFile.write(',\n')
    retrieveData(new)
    outputFile.write(',\n')
    retrieveData(hot)
        
    # Add comma unless it's the last entry
    if subreddit_index < len(subreddits) - 1:
        outputFile.write(',\n')

    # if(subreddit_index < len(subreddits) - 1):
        # print("sleeping for five seconds")
        # time.sleep(5)

outputFile.write("\n]")

outputFile.close()