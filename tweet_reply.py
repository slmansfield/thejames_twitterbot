import tweepy

# import logging
import time
import random

import pyheif
from PIL import Image

# import wallpaper
# import quote
import logger
import picture
import credentials

consumer_key = credentials.API_key
consumer_secret_key = credentials.API_secret_key
access_token = credentials.access_token
access_token_secret = credentials.access_token_secret

log = logger.createLogger()


def createApi():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    try:
        api.verify_credentials()
    except Exception as e:
        log.error("Error Creating API")
        raise e
    # logger.log.info("API Created")
    return api


def get_last_tweet(file):
    f = open(file, "r")
    lastId = int(f.read().strip())
    f.close()
    return lastId


def put_last_tweet(file, Id):
    f = open(file, "w")
    f.write(str(Id))
    f.close()
    log.info("Updated the file with the latest tweet Id")
    return


def respondToTweet(file="tweet_ID.txt"):
    api = createApi()
    last_id = get_last_tweet(file)
    mentions = api.mentions_timeline(last_id, tweet_mode="extended")
    if len(mentions) == 0:
        return

    new_id = 0
    log.info("someone mentioned me...")

    for mention in reversed(mentions):
        log.info(str(mention.id) + "-" + mention.full_text)
        new_id = mention.id

        if "#pod" in mention.full_text.lower():
            log.info("Responding back with POD to -{}".format(mention.id))
            try:
                # tweet = get_quote()
                # wallpaper.get_wallpaper(tweet)
                picture.getPicture()
                media = api.media_upload("images/temp.jpg")

                log.info("liking and replying to tweet")

                api.create_favorite(mention.id)
                log.info("liked tweet")
                api.update_status(
                    "@" + mention.user.screen_name + " Here's your Picture",
                    mention.id,
                    media_ids=[media.media_id],
                )
            except:
                log.info("Already replied to {}".format(mention.id))

    put_last_tweet(file, new_id)


def always_on():
    while True:
        respondToTweet()
        logger.log.info("Waiting...")
        time.sleep(120)
    respondToTweet()


if __name__ == "__main__":
    always_on()
