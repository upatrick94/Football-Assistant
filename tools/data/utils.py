import requests
from config import FOOTBALL_API_KEY
import unicodedata

base_url = "https://v3.football.api-sports.io"
headers = {"x-apisports-key": FOOTBALL_API_KEY}

LEAGUE_IDS = {
    "premier league": 39,
    "la liga": 140,
    "serie a": 135,
    "bundesliga": 78,
    "ligue 1": 61
}



TEAM_ALIASES = {
    "man utd": "manchester united",
    "manchester utd": "manchester united",
    "man city": "manchester city",
    "spurs": "tottenham",
    "newcastle united": "newcastle",
    "wolves": "wolverhampton",
    "west ham": "west ham united",
    "brighton": "brighton & hove albion",
    "nottingham forest": "nottm forest",


    "real madrid cf": "real madrid",
    "fc barcelona": "barcelona",
    "atletico madrid": "atlético madrid",


    "bayern munchen": "bayern munich",
    "fc bayern münchen": "bayern munich",
    "bayern münchen": "bayern munich",
    "rb leipzig": "leipzig",


    "inter milan": "inter",
    "ac milan": "milan",
    "napoli": "ssc napoli",
    "juve": "juventus",


    "psg": "paris saint germain",
    "paris sg": "paris saint germain",
}

def normalize_team_name(name: str):
    if not name:
        return ""
    name = unicodedata.normalize("NFD", name).encode("ascii", "ignore").decode("utf-8")
    name = name.lower().replace("fc ", "").replace("cf ", "").strip()
    if name in TEAM_ALIASES:
        name = TEAM_ALIASES[name]
    return name

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
    

KNOWN_TEAM_IDS = {
    "bayern munich": 157,
    "fc bayern münchen": 157,
    "bayern münchen": 157,
    "borussia dortmund": 165,
    "rb leipzig": 173,
    "bayer leverkusen": 168,

    "arsenal": 42,
    "manchester united": 33,
    "manchester city": 50,
    "liverpool": 40,
    "chelsea": 49,
    "tottenham": 47,

    "real madrid": 541,
    "barcelona": 529,
    "atletico madrid": 530,

    "inter": 505,
    "ac milan": 489,
    "juventus": 496,
    "napoli": 492,

    "paris saint germain": 85,
    "psg": 85,
}


def resolve_team_id(team_query, league_id=None, season=None):
    norm_query = normalize_team_name(team_query)

    if norm_query in KNOWN_TEAM_IDS:
        return KNOWN_TEAM_IDS[norm_query], team_query.title()

    try:
        resp = requests.get(
            f"{base_url}/teams",
            headers=headers,
            params={"search": team_query},
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"API request failed for '{team_query}': {e}")
        return None, None

    if not data.get("response"):
        print(f"No teams found for '{team_query}'.")
        return None, None

    candidates = data["response"]

    def is_womens_team(name):
        n = name.lower()
        return any(w in n for w in ["women", " ladies", " w", "(w)", "wfc"])

    filtered = [t for t in candidates if not is_womens_team(t["team"]["name"])]
    if not filtered:
        filtered = candidates 

    filtered.sort(
        key=lambda t: (
            normalize_team_name(t["team"]["name"]) == norm_query,
            norm_query in normalize_team_name(t["team"]["name"])
        ),
        reverse=True,
    )

    if league_id and season:
        for t in filtered:
            tid = t["team"]["id"]
            try:
                check = requests.get(
                    f"{base_url}/fixtures",
                    headers=headers,
                    params={"league": league_id, "season": season, "team": tid},
                    timeout=15,
                )
                j = check.json()
                if j.get("response"):
                    return tid, t["team"]["name"]
            except Exception:
                continue

    best = filtered[0]["team"]
    return best["id"], best["name"]
