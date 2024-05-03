# REMINDER: Reddit search engine should:
#               * Show relevant reddit posts given a search query (give weights to upvotes, titles, tags, etc)
#               * Have the ability to search by user name, or on "trending", "new", etc

import praw
import json
import config

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
subreddits = ["AskReddit", "worldnews", "todayilearned", "news", "science"]
for subreddit_index, subreddit in enumerate(subreddits):
    top = list(reddit.subreddit(subreddit).top(limit=500))
    for i, post in enumerate(top):
        # Retrieval of basic post information
        selftext = post.selftext
        authorname = post.author.name if post.author else 'deleted-user'
        title = post.title
        postID = post.id
        score = post.score
        imgurl = post.url
        permalink = post.permalink

        # Grabs five comments and their data
        comments_data = []
        for comment in post.comments[:10]:
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
            "permalink": permalink,
            "image url": imgurl,
            "comments": comments_data
        }

        json.dump(post_to_json, outputFile, indent=6)
        
        # Add comma unless it's the last entry
        if subreddit_index < len(subreddits) - 1 or i < len(top) - 1:
            outputFile.write(',\n')

outputFile.write("\n]")

outputFile.close()