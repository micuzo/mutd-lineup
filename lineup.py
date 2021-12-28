import http.client
import json
import os
from dotenv import load_dotenv
from datetime import datetime
from env import api_sport_keys
load_dotenv()

api_sport_base_url = "v3.football.api-sports.io"

#ids
mutd_id = 33
pl_id = 39
sample_mutd_game_id = 710741

def make_request(endpoint):
    conn = http.client.HTTPSConnection(api_sport_base_url)
    headers = {
    'x-rapidapi-host': api_sport_base_url,
    'x-rapidapi-key': api_sport_keys["API_KEY"]
    }
    today = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    conn.request("GET", endpoint, headers=headers)
    res = conn.getresponse()
    return json.loads(res.read().decode("utf8"))["response"]


def get_next_fixture(use_sample = False):
    data = {}
    if not use_sample:
        data = make_request(f"/fixtures?next=1&team={mutd_id}")
        return data[0]
    else:
        data = get_sample_next_fixture()[0]
        return data
        

def get_lineup(use_sample = False):
    data = {}
    if not use_sample:
        data = make_request(f"/fixtures/lineups?fixture={str(sample_mutd_game_id)}")
    else:
        data = get_sample_lineup()

    data = filter(lambda team : team["team"]["id"] == mutd_id, data)
    data = list(data)[0]
    map_func = lambda player : { "name": player["player"]["name"]}

    lineup = map(map_func, data["startXI"])
    return list(lineup)


def get_sample_lineup():
    f = open("sample/lineup.json")
    res = json.load(f)["response"]
    f.close()
    return res

def get_sample_next_fixture():
    f = open("sample/next-fixture.json")
    res = json.load(f)
    f.close()
    return res