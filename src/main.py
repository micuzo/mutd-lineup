import tweepy
import mulbot
from env import twitter_keys

auth = tweepy.OAuthHandler(twitter_keys["API_KEY"], twitter_keys["API_KEY_SECRET"])
auth.set_access_token(twitter_keys["ACCESS_TOKEN"], twitter_keys["ACCESS_TOKEN_SECRET"])
client = tweepy.Client(
    bearer_token = twitter_keys["BEARER_TOKEN"],
    consumer_key = twitter_keys["API_KEY"],
    consumer_secret = twitter_keys["API_KEY_SECRET"],
    access_token = twitter_keys["ACCESS_TOKEN"],
    access_token_secret = twitter_keys["ACCESS_TOKEN_SECRET"]
)

mulbot.main_exec(client)