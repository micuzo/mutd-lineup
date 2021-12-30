import json
import pytz
from datetime import datetime
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