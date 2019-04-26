import praw
import config as cf
import time
import tweepy
import urllib.request
import os
import schedule

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


# post jpg to twitter
def post_twitter(imagePath, title):
    api.update_with_media(imagePath, title)


# post submission url to twitter
def post_link_to_twitter(link):
    api.update_status(link)


# download image
def download_jpg(url, file_path, file_name):
    full_path = file_path + file_name + '.jpg'
    urllib.request.urlretrieve(url, full_path)


# run the bot
def run_bot():
    # find spicy memes
    for submission in reddit.subreddit('dankmemes').rising(limit=10):
        if submission.url.endswith(".jpg"):
            # download spicy memes
            download_jpg(submission.url, memes_folder, submission.id)
            print("submission with id " + submission.id + " saved to memes folder")

            # post spicy memes to twitter
            post_twitter(imagePath + submission.id + ".jpg", submission.title)
            print("posted" + imagePath + submission.id + ".jpg" + "to twitter" )
            # Delete spicy meme from meme folder
            os.remove(imagePath + submission.id + ".jpg")
            print("Deleted " + submission.id)
            # Wait ten seconds
            print("wating ten seconds....")
            time.sleep(10)
        else:
            # post link to twitter with the submission title
            post_link_to_twitter(submission.title + "  " + submission.url)
            print("posted link to twitter")


# runs bot every 3 hours
schedule.every(3).hours.do(run_bot)

while True:
    schedule.run_pending()
    time.sleep(1)