from datetime import datetime
from lineup import get_lineup

def create_tweet(client):
    lineup_txt = '\n'.join(list(map(lambda player: player["name"], get_lineup())))
    client.create_tweet(text=lineup_txt)
    print("Tweet created")
    

def get_mutd_tweet(client):
    manutd_user_id = "558797310"
    client.get_users_tweets(manutd_user_id, end_time="")