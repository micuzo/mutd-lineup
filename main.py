import os
import tweepy
from dotenv import load_dotenv
load_dotenv()

# Let's us authenticate bot account with our app

# Our keys
API_KEY = os.environ.get("API_KEY")
API_KEY_SECRET = os.environ.get("API_KEY_SECRET")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")

auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
client = tweepy.Client(
    bearer_token = BEARER_TOKEN,
    consumer_key = API_KEY,
    consumer_secret = API_KEY_SECRET,
    access_token = ACCESS_TOKEN,
    access_token_secret = ACCESS_TOKEN_SECRET
)

client.create_tweet(text="hello world!")

    