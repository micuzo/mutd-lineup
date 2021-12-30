import tweepy
import mulbot
import lineup
import sys
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

args = sys.argv[1:]
if len(args) == 0 or args[0] == '-mulbot':
    mulbot.main_exec(client)
elif args[0] == '-lineup':
    lineup.main_exec()
elif args[0] == '-h':
    help_str = '''Options
    -lineup   update information in out.json
    -mulbot   check if lineup is out and tweet it'''
    print(help_str)
else:
    print("Wrong paramters")