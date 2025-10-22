from tools.data.utils import get_league_id, make_request

def get_upcoming_fixtures(team_name, league_name="Premier League", season=2023, limit=5):
    league_id = get_league_id(league_name)

    team_search = make_request("teams", {"search": team_name})
    if not team_search or not team_search.get("response"):
        print(f"Team '{team_name}' not found.")
        return None
    team_id = team_search["response"][0]["team"]["id"]
    team_name = team_search["response"][0]["team"]["name"]

    fixtures_data = make_request("fixtures", {"league": league_id, "season": season, "team": team_id})
    if not fixtures_data or not fixtures_data.get("response"):
        print(f"No fixture data found for {team_name} in {league_name}.")
        return None
    
    fixtures = fixtures_data["response"]
    upcoming = [f for f in fixtures if f["fixture"]["status"]["short"] in ("NS", "TBD", "PST")]
    if not upcoming:
        print(f"No upcoming fixtures for {team_name}, showing last matches instead.")
        upcoming = sorted(fixtures, key=lambda f: f["fixture"]["date"], reverse=True)[:limit]
    else:
        upcoming = sorted(upcoming, key=lambda f: f["fixture"]["date"])[:limit]

    clean_fixtures = []
    for match in upcoming:
        fx = match["fixture"]
        home = match["teams"]["home"]["name"]
        away = match["teams"]["away"]["name"]
        venue = fx["venue"]["name"] if fx["venue"] else "Unknown Venue"
        clean_fixtures.append({
            "date": fx["date"][:10],
            "home": home,
            "away": away,
            "venue": venue,
            "status": "Home" if home == team_name else "Away",
            "match_status": fx["status"]["short"]
        })

    return {"team": team_name, "fixtures": clean_fixtures}
