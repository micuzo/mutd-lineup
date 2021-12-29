import os
from dotenv import load_dotenv
load_dotenv()

twitter_keys = {
    "API_KEY": os.environ.get("API_KEY"),
    "API_KEY_SECRET": os.environ.get("API_KEY_SECRET"),
    "ACCESS_TOKEN": os.environ.get("ACCESS_TOKEN"),
    "ACCESS_TOKEN_SECRET": os.environ.get("ACCESS_TOKEN_SECRET"),
    "BEARER_TOKEN": os.environ.get("BEARER_TOKEN")
}

api_sport_keys = {
    "API_KEY": os.environ.get("API_SPORT_KEY")
}

is_prod = os.environ.get("ENV") == "PROD"