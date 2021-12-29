from datetime import datetime, timedelta
from helper import min_item, to_datetime
from lineup import get_lineup, get_next_fixture
from env import is_prod

def create_tweet(client):
    lineup_txt = '\n'.join(list(map(lambda player: player["name"], get_lineup(True))))
    lineup_tweet = get_mutd_tweet(client)
    #client.create_tweet(text=lineup_txt, in_reply_to_tweet_id=lineup_tweet)
    print("Tweet created")
    

def get_mutd_tweet(client):
    manutd_user_id = "558797310" if is_prod else "1475931923511980033"
    tweets = client.get_users_tweets(manutd_user_id, max_results=5,tweet_fields=["created_at"]).data

    # Find united tweet closest to expected lineup relsease time

    # Some ids
    pl_id = 39
    ucl_id = 2
    fa_cup_id = 45
    league_cup_id = 48

    lineup_release_offset = {
        pl_id: 60,
        ucl_id: 75,
        fa_cup_id: 60,
        league_cup_id: 60
    }
    next_fixutre = get_next_fixture(True)
    next_date = next_fixutre['fixture']['date']
    offset = lineup_release_offset[next_fixutre['league']['id']]
    print()

    #print((datetime.fromisoformat(tweets[0].created_at)))
    #closest_tweet = min_item(lambda tweet : to_datetime(next_date) - timedelta(minutes=offset))

    #print(to_datetime(next_date) - timedelta(minutes=offset))
    return tweets[len(tweets) - 1].id

def test(client):
    return get_next_fixture(True)['fixture']['date']