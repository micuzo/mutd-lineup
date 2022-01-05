import pytz
from env import FORCE_TWEET
from datetime import datetime
from helper import get_logger, get_next_fixture_info, write_out_json, read_out_json, twitter_ids
from lineup import get_lineup
from functools import cmp_to_key

#Replies to @ManUTD with the lineup for the game
def create_tweet(client, lineup_tweet_id, team_lineup):
    logger = get_logger()
    player_names = list(map(lambda player : player["name"], team_lineup))
    lineup_txt = '\n'.join(player_names)
    client.create_tweet(text=lineup_txt, in_reply_to_tweet_id=lineup_tweet_id)
    logger.info(f'Replied to tweet {lineup_tweet_id} with lineup')



# Gets the @ManUtd tweet id with the timestamp that is the closest to
# when lineups are expected to be released
def get_lineup_tweet_id(client, release_time):
    logger = get_logger()
    MANUTD_ID = twitter_ids['MANUTD']
    tweets = client.get_users_tweets(MANUTD_ID, user_auth=True, max_results=5,tweet_fields=["created_at"]).data

    def compare_func(tw1, tw2):
        tw1_diff = (release_time - tw1.created_at).total_seconds()
        tw2_diff = (release_time - tw2.created_at).total_seconds()
        return abs(tw1_diff) - abs(tw2_diff)

    tweet = min(tweets, key=cmp_to_key(compare_func))
    logger.info(f'Choosing tweet [{tweet.created_at}] - {tweet.id}: {tweet.text}')
    return tweet.id



#If we are before release time exit program
#else if we can tweet and we are before kick off, tweet lineup
def main_exec(client):
    data = read_out_json()
    logger = get_logger()

    if not data or not data['can_tweet']:
        if not data: logger.warning('Did not find out.json')
        elif not data['can_tweet']: logger.debug('Already tweeted, cannot tweet')
        return
    
    next_fixture_info = get_next_fixture_info(data)
    t = datetime.now(tz=pytz.timezone('Europe/London'))
    
    #Tweet if we should
    if t < next_fixture_info['lineup_release_time'] and not FORCE_TWEET:
        logger.debug(f"Script run before release time: {t} < {next_fixture_info['lineup_release_time']}")
        return
    
    elif t < next_fixture_info['kick_off'] or FORCE_TWEET:
        team_lineup = get_lineup(next_fixture_info['id'])

        if team_lineup is None:
            logger.info(f'No lineup was found')
            return

        lineup_tweet_id = get_lineup_tweet_id(client, next_fixture_info['lineup_release_time'])

        try:
            create_tweet(client, lineup_tweet_id, team_lineup)
        except:
            logger.exception('Tweet could not be created')
            return
        
        logger.info('Setting can_tweet to False...')
        write_out_json(keyval=('can_tweet', False))
    
    elif t > next_fixture_info['kick_off']:
        logger.info('Passed kick off, probably postponed, exiting')