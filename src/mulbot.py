import pytz
from datetime import datetime, timedelta
from helper import min_item, to_datetime, api_sport_ids
from lineup import get_lineup, get_next_fixture
from env import is_prod

#Replies to @ManUTD with the lineup for the game
def create_tweet(client, lineup_tweet_id):
    lineup_txt = '\n'.join(list(map(lambda player : player["name"], get_lineup(True))))
    client.create_tweet(text=lineup_txt, in_reply_to_tweet_id=lineup_tweet_id)
    
# Gets the @ManUtd tweet id with the timestamp that is the closest to
# when lineups are expected to be released
def get_lineup_tweet_id(client, next_fixture_date, release_offset):
    manutd_user_id = "558797310" if is_prod else "1475931923511980033"
    tweets = client.get_users_tweets(manutd_user_id, user_auth=True, max_results=5,tweet_fields=["created_at"]).data

    def map_func(tw):
        release_time = next_fixture_date - timedelta(minutes=release_offset)
        return (release_time - tw.created_at).total_seconds()

    tweet = min_item(map_func, tweets)
    return tweet.id

lineup_release_offset = {
    api_sport_ids["PL"]: 60,
    api_sport_ids["UCL"]: 75,
    api_sport_ids["FA_CUP"]: 60,
    api_sport_ids["LEAGUE_CUP"]: 60
}

# Get when next lineup is exprected to release
# Idle until 30 seconds after time
# Get lineup from api_sport
# Tweet lineup
def main_exec(client):
    print("Getting next fixture...")
    next_fixture = get_next_fixture(True)
    next_fixture_date = to_datetime(next_fixture['fixture']['date'])
    next_fixture_league_id = next_fixture["league"]["id"]
    
    print("Getting tweet with closes timestamp to expected lineup release time...")
    lineup_tweet_id = get_lineup_tweet_id(client, next_fixture_date, lineup_release_offset[next_fixture_league_id])

    print("Replying to tweet with lineup...")
    create_tweet(client, lineup_tweet_id)
    print("Tweet Created!")
