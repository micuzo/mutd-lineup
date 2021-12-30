import http.client
import json
from dotenv import load_dotenv
from env_type import api_sport_keys, env_type
from helper import api_sport_ids
from functools import cmp_to_key
load_dotenv()

api_sport_base_url = "v3.football.api-sports.io"

# Write to out.json:
#   - next fixture
#   - whether or not we can tweet
def main_exec():
    next_fixture = get_next_fixture()
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


def get_next_fixture():
    data = {}
    if env_type['api_sport_env'] == 'PROD':
        data = make_request(f'/fixtures?next=1&team={api_sport_ids["MANUTD"]}&timezone=Europe/London')
        return data[0]
    else:
        data = get_sample_next_fixture()[0]
        return data
        

def get_lineup():
    data = {}
    if env_type['api_sport_env'] == 'PROD':
        data = make_request(f"/fixtures/lineups?fixture={str(api_sport_ids['SAMPLE_FIXTURE'])}")
    else:
        data = get_sample_lineup()

    data = filter(lambda team : team["team"]["id"] == api_sport_ids['MANUTD'], data)
    data = list(data)[0]
    map_func = lambda player : { 
        "name": player["player"]["name"],
        "grid": player["player"]["grid"]
    }

    lineup = list(map(map_func, data["startXI"]))

    # example: Degea would have [1:1], Dalot[2:4]
    def compare_func(p1, p2):
        grid_i1 = p1['grid'].split(':')[0]
        grid_i2 = p2['grid'].split(':')[0]
        
        grid_j1 = p1['grid'].split(':')[1]
        grid_j2 = p2['grid'].split(':')[1]

        if grid_i1 == grid_i2:
            return int(grid_j1) - int(grid_j2)
        else:
            return int(grid_i1) - int(grid_i2)
        
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