import logging
import json
import pytz
import sys
from datetime import datetime, timedelta
from env import env_type

# CONSTANTS
twitter_ids = {
    'MANUTD': '558797310' if env_type['twitter_env'] == 'PROD' else '1475931923511980033'
}

api_sport_ids = {
    "PL": 39,
    "UCL": 2,
    "FA_CUP": 45,
    "LEAGUE_CUP": 48,
    "MANUTD": 33,
    "SAMPLE_FIXTURE": 710741
}

lineup_release_offset = {
    api_sport_ids["PL"]: 60,
    api_sport_ids["UCL"]: 75,
    api_sport_ids["FA_CUP"]: 60,
    api_sport_ids["LEAGUE_CUP"]: 60
}


# FUNCTIONS

# format example: 2021-12-30T20: 15: 00+00: 00
# should look into datetime.strptime
def to_datetime(timestamp:str):
    dt = timestamp.replace(' ', '')
    date = dt.split('T')[0]
    time = dt.split('T')[1]

    date = date.split('-')
    date = list(map(lambda d : int(d), date))

    time = [time.split(':')[0], time.split(':')[1]]
    time = list(map(lambda t : int(t), time))

    return datetime(date[0], date[1], date[2], time[0], time[1]).replace(tzinfo=pytz.UTC)

def write_out_json(data=None, keyval=None):
    if data is None and keyval is not None:
        data = read_out_json()
        data[keyval[0]] = keyval[1]
        
    f = open('../out.json', 'w')
    f.write(json.dumps(data))
    f.close()

def read_out_json(key=''):
    f = open('../out.json', 'r')
    data = json.load(f)
    f.close()
    res =  data[key] if key != '' else data
    return res


def get_next_fixture_info(data):
    next_fixture = data['fixture']
    next_fixture_kickoff = to_datetime(next_fixture['fixture']['date'])
    next_fixture_league_id = next_fixture["league"]["id"]
    release_time = next_fixture_kickoff - timedelta(minutes=lineup_release_offset[next_fixture_league_id] - 5)
    
    return {
        'id': next_fixture['fixture']['id'],
        'kick_off': next_fixture_kickoff,
        'league_id': next_fixture_league_id,
        'lineup_release_time': release_time
    }

loggers = set()
def get_logger():
    args = sys.argv[1:]
    name = 'main-logger'
    if len(args) == 0 or args[0] == '-mulbot':
        name = 'mulbot'
    elif args[0] == '-lineup':
        name = 'lineup'
    else:
        exit()

    logger = logging.getLogger(name)
    if name in loggers:
        return logger
    else:
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s %(message)s')

        file_handler = logging.FileHandler(f'../{name}.log')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)

        file_handler_debug = logging.FileHandler(f'../{name}-debug.log')
        file_handler_debug.setLevel(logging.DEBUG)
        file_handler_debug.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(file_handler_debug)
        loggers.add(name)
    
    return logger