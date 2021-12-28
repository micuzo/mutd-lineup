import http.client
import json
import os
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()

api_sport_base_url = "v3.football.api-sports.io"
API_SPORT_KEY = os.environ.get("API_SPORT_KEY")

#ids
mutd_id = 33
pl_id = 39
sample_mutd_game_id = 710741

def make_request():
    conn = http.client.HTTPSConnection(api_sport_base_url)
    headers = {
    'x-rapidapi-host': api_sport_base_url,
    'x-rapidapi-key': API_SPORT_KEY
    }
    today = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    conn.request("GET", f"/fixtures/lineups?fixture={str(sample_mutd_game_id)}", headers=headers)
    res = conn.getresponse()

    data = json.loads(res.read().decode("utf8"))["response"]

    for team in data:
        team_id = team["team"]["id"]
        if team_id == mutd_id:
            conn.close()
            return team

def get_sample():
    f = open("sample/lineup.json")
    for team in json.load(f)["response"]:
        team_id = team["team"]["id"]
        if team_id == mutd_id:
            f.close()
            return team

def get_lineup(data = None):
    if data is None:
        data = get_sample()
    def map_func(player):
        return {
            "name": player["player"]["name"]
        }

    lineup = map(map_func, data["startXI"])
    return list(lineup)