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
    
def resolve_team_id(team_query: str, league_id: int | None = None, season: int | None = None):
    data = make_request("teams", {"search": team_query})
    if not data or not data.get("response"):
        return None, None
    
    candidates = data["response"]

    def is_womens(name: str):
        n = name.lower()
        return " women" in n or n.endswith(" w") or n.endswith(" w.") or n == "women"
    
    filtered = [t for t in candidates if not is_womens(t["team"]["name"])]

    if not filtered:
        filtered = candidates

    q = team_query.lower().replace("munich", "münchen")
    def score(t):
        name = t["team"]["name"]
        s = 0
        if q == name: s+=100
        if q in name: s+=50
        if "fc " + q in name: s+=20
        if " w" in name or "women" in name: s=-20
        return s
    
    filtered.sort(key=score, reverse=True)

    if league_id and season:
        best = None
        for t in filtered:
            tid = t["team"]["id"]
            fx = make_request("fixtures", {"league": league_id, "season": season, "team": tid})
            if fx and fx.get("response"):
                best = t
                break

        if best:
            return best["team"]["id"], best["team"]["name"]
        
    return filtered[0]["team"]["id"], filtered[0]["team"]["name"]