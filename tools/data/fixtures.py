from tools.data.utils import get_league_id, make_request, resolve_team_id

def get_upcoming_fixtures(team_name, league_name="Premier League", season=2023, limit=5):
    league_id = get_league_id(league_name)
    team_id, resolved_name = resolve_team_id(team_name, league_id, season)
    if not team_id:
        print(f"Team '{team_name}' not found.")
        return None
    
    data = make_request("fixtures", {"league": league_id, "season": season, "team": team_id})
    if not data or not data.get("response"):
        print(f"No fixture data found for {team_name} in {league_name}.")
        return None
    
    upcoming_status = {"TBD", "NS", "PST"}
    upcoming = [m for m in data["response"] if m["fixture"]["status"]["short"] in upcoming_status]
    upcoming.sort(key=lambda m: m["fixture"]["date"])
    upcoming = upcoming[:limit]

    if not upcoming:
        finished = [m for m in data["response"] if m["fixture"]["status"]["short"] in {"FT", "AET", "PEN"}]
        finished.sort(key=lambda m: m["fixture"]["date"], reverse=True)
        if not finished:
            print(f"No upcoming or finished fixtures for {resolved_name}.")
            return None
        print(f"No upcoming fixtures for {resolved_name}, showing last matches instead.")

        clean = []
        for m in finished:
            fx = m["fixture"]
            home = m["teams"]["home"]["name"]
            away = m["teams"]["away"]["name"]
            venue = fx["venue"]["name"] if fx["venue"] else "Unknown venue"
            clean.append({
                "date": fx["date"][:10],
                "home": home,
                "away": away,
                "venue": venue,
                "status": "Home" if home ==resolved_name else "Away",
                "match_status": fx["status"]["short"]
            })
        return {"team": resolved_name, "fixtures": clean}
    
    clean = []
    for m in upcoming:
        fx = m["fixture"]
        home = m["teams"]["home"]["name"]
        away = m["teams"]["away"]["name"]
        venue = fx["venue"]["name"] if fx["venue"] else "Unknown Venue"
        clean.append({
            "date": fx["date"][:10],
            "home": home,
            "away": away,
            "venue": venue,
            "status": "Home" if home == resolved_name else "Away",
            "match_status": fx["status"]["short"],
        })

    return {"team": resolved_name, "fixtures": clean}
