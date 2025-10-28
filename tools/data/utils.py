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

TEAM_ALIASES = {
    "bayern munich": "bayern",
    "fc bayern münchen": "bayern",
    "bayern münchen": "bayern",
    "psg": "paris saint germain",
    "inter milan": "inter",
    "ac milan": "ac milan",
    "man utd": "manchester united",
    "manchester utd": "manchester united",
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
    
def resolve_team_id(team_query: str, league_id=None, season=None):
    import unicodedata

    team_query = team_query.strip().lower()
    team_query = TEAM_ALIASES.get(team_query, team_query)

    team_ascii = unicodedata.normalize("NFD", team_query).encode("ascii", "ignore").decode("utf-8")

    search_terms = list({team_query, team_ascii, team_query.replace("munich", "bayern")})

    candidates = []
    for term in search_terms:
        resp = requests.get(
            f"{base_url}/teams",
            headers=headers,
            params={"search": term},
            timeout=15
        )
        if not resp.ok:
            continue
        data = resp.json()
        if data.get("response"):
            candidates.extend(data["response"])

    if not candidates:
        print(f"⚠️ No teams found for '{team_query}'. Tried: {search_terms}")
        return None, None

    seen = set()
    filtered = []
    for t in candidates:
        name = t["team"]["name"]
        if name.lower() in seen:
            continue
        seen.add(name.lower())

        lower_name = name.lower()
        if any(w in lower_name for w in ["women", " ladies", " w", "(w)", "wfc"]):
            continue
        filtered.append(t)

    if not filtered:
        filtered = candidates

    filtered.sort(key=lambda t: "bayern" in t["team"]["name"].lower(), reverse=True)

    if league_id and season:
        for t in filtered:
            tid = t["team"]["id"]
            check = requests.get(
                f"{base_url}/fixtures",
                headers=headers,
                params={"league": league_id, "season": season, "team": tid},
                timeout=15
            ).json()
            if check.get("response"):
                return tid, t["team"]["name"]

    best = filtered[0]["team"]
    return best["id"], best["name"]