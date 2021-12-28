import os
import tweepy
from dotenv import load_dotenv
from lineup import get_lineup
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

lineup = get_lineup()
lineup_txt = '\n'.join(list(map(lambda player: player["name"], get_lineup())))
client.create_tweet(text=lineup_txt)
print("Tweet created")

manutd_user_id = "558797310"