import pytz
from env import FORCE_TWEET
from datetime import datetime, timedelta
from helper import to_datetime, lineup_release_offset, write_out_json, read_out_json, twitter_ids
from lineup import get_lineup
from functools import cmp_to_key

#Replies to @ManUTD with the lineup for the game
def create_tweet(client, lineup_tweet_id, team_lineup):
    player_names = list(map(lambda player : player["name"], team_lineup))
    lineup_txt = '\n'.join(player_names)
    client.create_tweet(text=lineup_txt, in_reply_to_tweet_id=lineup_tweet_id)
    


# Gets the @ManUtd tweet id with the timestamp that is the closest to
# when lineups are expected to be released
def get_lineup_tweet_id(client, release_time):
    MANUTD_ID = twitter_ids['MANUTD']
    tweets = client.get_users_tweets(MANUTD_ID, user_auth=True, max_results=5,tweet_fields=["created_at"]).data

    def compare_func(tw1, tw2):
        tw1_diff = (release_time - tw1.created_at).total_seconds()
        tw2_diff = (release_time - tw2.created_at).total_seconds()
        return abs(tw1_diff) - abs(tw2_diff)

    tweet = min(tweets, key=cmp_to_key(compare_func))
    return tweet.id



#If we are before release time exit program
#else if we can tweet and we are before kick off, tweet lineup
def main_exec(client):
    t = datetime.now(tz=pytz.timezone('Europe/London'))
    data = read_out_json()
    
    #next fixture info
    next_fixture = data['fixture']
    next_fixture_date = to_datetime(next_fixture['fixture']['date'])
    next_fixture_league_id = next_fixture["league"]["id"]

    release_time = next_fixture_date - timedelta(minutes=lineup_release_offset[next_fixture_league_id] - 5)

    if not data or t < release_time and not FORCE_TWEET:
        msg = "Could not get data from out.json..." if not data else f"Script run before release time: {t} < {release_time}"
        print(msg)
        exit()
    elif data and data['can_tweet'] and t < next_fixture_date:
        print("Getting team lineup...")
        team_lineup = get_lineup(next_fixture['fixture']['id'])

        if team_lineup is None:
            print('No lineup was found, exiting...')
            exit()

        print("Getting tweet with closest timestamp to expected release time...")
        lineup_tweet_id = get_lineup_tweet_id(client, release_time)

        print("Replying to tweet with lineup...")
        try:
            create_tweet(client, lineup_tweet_id, team_lineup)
        except:
            print('Tweet could not be created')
            exit()
        
        print("Tweet Created!")

        if not FORCE_TWEET:
            print('Setting can_tweet to False...')
            write_out_json(keyval=('can_tweet', False))