import http.client
import json
from dotenv import load_dotenv
from env import api_sport_keys
from helper import api_sport_ids
from functools import cmp_to_key
load_dotenv()

api_sport_base_url = "v3.football.api-sports.io"

# Write to out.json:
#   - next fixture
#   - whether or not we can tweet
def main_exec():
    next_fixture = get_next_fixture(True)
    data = {'can_tweet': True}
    f = open ('../out.json', 'r')
    read_data = json.load(f)

    if read_data and read_data['fixture']['fixture']['id'] != next_fixture['fixture']['id']:
        data['can_tweet'] = True
    elif read_data:
        data["can_tweet"] = read_data['can_tweet']
        
    data['fixture'] = next_fixture
    f.close()
    
    f = open('../out.json', 'w')
    f.write(json.dumps(data))
    f.close()

def make_request(endpoint):
    conn = http.client.HTTPSConnection(api_sport_base_url)
    headers = {
    'x-rapidapi-host': api_sport_base_url,
    'x-rapidapi-key': api_sport_keys["API_KEY"]
    }
    conn.request("GET", endpoint, headers=headers)
    res = conn.getresponse()
    return json.loads(res.read().decode("utf8"))["response"]


def get_next_fixture(use_sample = False):
    data = {}
    if not use_sample:
        data = make_request(f'/fixtures?next=1&team={api_sport_ids["MANUTD"]}&timezone=Europe/London')
        return data[0]
    else:
        data = get_sample_next_fixture()[0]
        return data
        

def get_lineup(use_sample = False):
    data = {}
    if not use_sample:
        data = make_request(f"/fixtures/lineups?fixture={str(api_sport_ids['SAMPLE_FIXTURE'])}")
    else:
        data = get_sample_lineup()

    data = filter(lambda team : team["team"]["id"] == api_sport_ids['MANUTD'], data)
    data = list(data)[0]
    map_func = lambda player : { 
        "name": player["player"]["name"],
        "grid": player["player"]["grid"],
        "pos": player["player"]["pos"] 
    }

    lineup = list(map(map_func, data["startXI"]))

    def compare_func(p1, p2):
        pos_values = {
            "G": 0,
            "D": 1,
            "M": 2,
            "F": 3
        }
        pos1 = pos_values[p1["pos"]]
        pos2 = pos_values[p2["pos"]]
        grid_sum1 = sum(list(map(lambda grid_pos : int(grid_pos), p1["grid"].split(":"))))
        grid_sum2 = sum(list(map(lambda grid_pos : int(grid_pos), p2["grid"].split(":"))))

        if pos1 == pos2:
            return grid_sum1 - grid_sum2
        else:
            return pos1 - pos2
        
    return sorted(lineup, key=cmp_to_key(compare_func))


def get_sample_lineup():
    f = open("../sample/lineup.json")
    res = json.load(f)["response"]
    f.close()
    return res

def get_sample_next_fixture():
    f = open("../sample/next-fixture.json")
    res = json.load(f)
    f.close()
    return res