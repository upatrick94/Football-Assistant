import requests
from config import FOOTBALL_API_KEY

base_url = "https://v3.football.api-sports.io"
headers = {"x-apisports-key": FOOTBALL_API_KEY}

LEAGUE_IDS = {
    "premier league": 39,
    "la liga": 140,
    "serie a": 135,
    "bundesliga": 78,
    "ligue 1": 61
}

def get_league_id(league_name: str):
    name = league_name.lower().strip()
    for key,value in LEAGUE_IDS.items():
        if key in name:
            return value
    return LEAGUE_IDS["premier league"]

def make_request(endpoint: str, params: dict):
    try:
        response = requests.get(f"{base_url}/{endpoint}", headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f" API request failed ({endpoint}): {e}")
        return None