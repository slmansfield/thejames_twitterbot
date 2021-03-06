# install external python modules
import tweepy
import time
import os

# install local python modules
from logger import logger as log
import picture

consumer_key = os.getenv("API_KEY")
consumer_secret_key = os.getenv("API_KEY_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

log = logger.create_logger()

def create_api():
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

def follow_followers(api):
    log.info("Retrieving and following followers")
    for follower in tweepy.Cursor(api.followers).items():
        if not follower.following:
            log.info(f"Following {follower.screen_name}")
            follower.follow()
            # adding a mention to welcome new follower
            # api.update_status(
            #         "@" + follower.screen_name + " Welcome to TheJames"verse"", All Hail King James!)
        else:
            log.info("no new followers")

def create_tweet(api, mention):
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
    finally:
        os.remove("images/temp.jpg")

def respond_to_tweet(api, file="tweet_ID.txt"):
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
            log.info("Responding back with {} to -{}".format("pod", mention.id))
            create_tweet(api, mention)
        elif "#jamesforall" in mention.full_text.lower():
            log.info("Responding back with {} to -{}".format("jamesforall", mention.id))
            create_tweet(api, mention)
        elif "#allhailthejames" in mention.full_text.lower():
            log.info("Responding back with {} to -{}".format("allhailthejames", mention.id))
            create_tweet(api, mention)

    put_last_tweet(file, new_id)

def always_on():
    while True:
        api = create_api()
        follow_followers(api)
        respond_to_tweet(api)
        log.info("Waiting...")
        time.sleep(60)
    

if __name__ == "__main__":
    always_on()
