import pytz
from datetime import datetime, timedelta
from helper import to_datetime, lineup_release_offset, write_out_json, read_out_json
from lineup import get_lineup
from env import is_prod
from functools import cmp_to_key

#Replies to @ManUTD with the lineup for the game
def create_tweet(client, lineup_tweet_id, team_lineup):
    player_names = list(map(lambda player : player["name"], team_lineup))
    lineup_txt = '\n'.join(player_names)
    client.create_tweet(text=lineup_txt, in_reply_to_tweet_id=lineup_tweet_id)
    


# Gets the @ManUtd tweet id with the timestamp that is the closest to
# when lineups are expected to be released
def get_lineup_tweet_id(client, release_time):
    manutd_user_id = "558797310" if is_prod else "1475931923511980033"
    tweets = client.get_users_tweets(manutd_user_id, user_auth=True, max_results=5,tweet_fields=["created_at"]).data

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

    if not data or t < release_time:
        msg = "Could not get data from out.json..." if not data else f"Script run before release time: {t} < {release_time}"
        print(msg)
        exit()
    elif data and data['can_tweet'] and t < next_fixture_date:
        print('Setting can_tweet to False...')
        write_out_json(keyval=('can_tweet', False))
        
        print("Getting team lineup...")
        team_lineup = get_lineup(True)

        print("Getting tweet with closest timestamp to expected release time...")
        lineup_tweet_id = get_lineup_tweet_id(client, release_time)

        print("Replying to tweet with lineup...")
        create_tweet(client, lineup_tweet_id, team_lineup)
        print("Tweet Created!")