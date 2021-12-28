import http.client
import os
from dotenv import load_dotenv
load_dotenv()

api_sport_base_url = "v3.football.api-sports.io"
API_SPORT_KEY = os.environ.get("API_SPORT_KEY")


conn = http.client.HTTPSConnection(api_sport_base_url)
headers = {
    'x-rapidapi-host': api_sport_base_url,
    'x-rapidapi-key': API_SPORT_KEY
}

conn.request("GET", "/teams?id=33", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
conn.close()