import http.client
import json
from dotenv import load_dotenv
from env import api_sport_keys, env_type
from helper import api_sport_ids, write_out_json, read_out_json
from functools import cmp_to_key
load_dotenv()

api_sport_base_url = "v3.football.api-sports.io"

# Write to out.json:
#   - next fixture
#   - whether or not we can tweet
def main_exec():
    next_fixture = get_next_fixture()

    if next_fixture is None:
        print('no fixture was found, writing empty json object...')
        write_out_json({})
        return

    new_data = {'can_tweet': True}
    print('Reading data currently in out.json...')
    read_data = read_out_json()

    if read_data and read_data['fixture']['fixture']['id'] != next_fixture['fixture']['id']:
        print('The next fixture is different to the one currently stored, setting can_tweet to true...')
        new_data['can_tweet'] = True
    elif read_data:
        print('The next fixture is the same as the one currently stored, keeping same can_tweet value...')
        new_data["can_tweet"] = read_data['can_tweet']
        
    new_data['fixture'] = next_fixture
    print('Overwriting data in out.json...')
    write_out_json(new_data)



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
        return data[0] if len(data) > 0 else None
    else:
        data = get_sample_next_fixture()[0]
        return data
        

def get_lineup(next_fixture_id):
    data = {}
    if env_type['api_sport_env'] == 'PROD':
        data = make_request(f"/fixtures/lineups?fixture={next_fixture_id}")
    else:
        data = get_sample_lineup()

    if len(data) == 0:
        return None

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