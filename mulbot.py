from datetime import datetime
from lineup import get_lineup, get_next_fixture

def create_tweet(client):
    lineup_txt = '\n'.join(list(map(lambda player: player["name"], get_lineup(True))))
    client.create_tweet(text=lineup_txt)
    print("Tweet created")
    

def get_mutd_tweet(client):
    manutd_user_id = "558797310"
    return client.get_users_tweets(manutd_user_id, max_results=5)

def test():
    return get_next_fixture(True)