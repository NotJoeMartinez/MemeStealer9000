import praw
import config as cf
import time
import tweepy

reddit = praw.Reddit(client_id=cf.client_id,
                     client_secret=cf.client_secret,
                     user_agent=cf.user_agent,
                     username=cf.username,
                     password=cf.password)




auth = tweepy.OAuthHandler(cf.CONSUMER_KEY, cf.CONSUMER_SECRET)
auth.set_access_token(cf.ACCESS_KEY, cf.ACCESS_SECRET)
api = tweepy.API(auth)

BASE_URL = 'https://www.reddit.com'

# find images of a set amount of upvotes

def bot():
    for submission in reddit.front.hot(limit=10):
        if submission.score > 150:
            api.update_status(BASE_URL + submission.permalink)
            print(BASE_URL + submission.permalink + "was posted to twitter")
            time.sleep(10)


# repost said images to twitter


while True:
    bot()
