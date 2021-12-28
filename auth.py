import os
import tweepy
from dotenv import load_dotenv

load_dotenv()

# Let's us authenticate bot account with our app

# Our keys
API_KEY = os.environ.get("API_KEY")
API_KEY_SECRET = os.environ.get("API_KEY_SECRET")

auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET, "oob")
verifier = ""

try:
    redirect_url = auth.get_authorization_url()
    print(redirect_url)
    verifier = input("Verifier: ")
except tweepy.TweepError:
    print('Error! Failed to get request token.')

try:
    auth.get_access_token(verifier)
    api = tweepy.API(auth)
    print(auth.access_token, auth.access_token_secret)
except tweepy.TweepError:
    print('Error! Failed to get access token.')