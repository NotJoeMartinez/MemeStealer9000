import praw
import config as cf
import time
import tweepy
import urllib.request
import os

# reddit api
reddit = praw.Reddit(client_id=cf.client_id,
                     client_secret=cf.client_secret,
                     user_agent=cf.user_agent,
                     username=cf.username,
                     password=cf.password)

# twitter api
auth = tweepy.OAuthHandler(cf.CONSUMER_KEY, cf.CONSUMER_SECRET)
auth.set_access_token(cf.ACCESS_KEY, cf.ACCESS_SECRET)
api = tweepy.API(auth)

BASE_URL = 'https://www.reddit.com'
memes_folder = "/memes"  # path to local memes folder
imagePath = memes_folder


# post to twitter
def post_twitter(imagePath):
    api.update_with_media(imagePath)


# download image
def download_jpg(url, file_path, file_name):
    full_path = file_path + file_name + '.jpg'
    urllib.request.urlretrieve(url, full_path)


# run the bot
def run_bot():
    # find the spicy memes
    for submission in reddit.subreddit('dankmemes').hot(limit=10):
        # filter out any non jpg images
        if submission.url.endswith(".jpg"):
            # download spicy memes
            download_jpg(submission.url, memes_folder, submission.id)
            print("submission with id " + submission.id + " saved to memes folder")

            # try to post spicy memes to twitter
            post_twitter(imagePath + submission.id + ".jpg")
            print("posted" + submission.id + ".jpg" + "to twitter")
            print("waiting ten seconds...")
            time.sleep(10)
        else:
            print("not a jpg")


while True:
    run_bot()
