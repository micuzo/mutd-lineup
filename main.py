import os
import tweepy
from dotenv import load_dotenv
from lineup import get_lineup

load_dotenv()

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

lineup = get_lineup()
lineup_txt = '\n'.join(list(map(lambda player: player["name"], get_lineup())))
client.create_tweet(text=lineup_txt)
print("Tweet created")

manutd_user_id = "558797310"