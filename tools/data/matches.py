from tools.data.utils import make_request, get_league_id, resolve_team_id, normalize_team_name
import unicodedata


def get_team_recent_matches(team_name, league_name="Premier League", season=2023, last_n=5):
    league_id = get_league_id(league_name)
    team_id, resolved_name = resolve_team_id(team_name, league_id, season)
    if not team_id:
        print(f"Team '{team_name}' not found.")
        return None
    
    data = make_request("fixtures", {"league": league_id, "season": season, "team": team_id})
    if not data or not data.get("response"):
        print(f"No fixtures found for {team_name} in {league_name}.")
        return None
    
    finished = [m for m in data["response"] if m["fixture"]["status"]["short"] in {"FT", "AET", "PEN"}]
    finished.sort(key=lambda m: m["fixture"]["date"], reverse=True)
    finished = finished[:last_n]

    clean = []
    norm_team = normalize_team_name(resolved_name)
    for m in finished:
        fx = m["fixture"]
        home = m["teams"]["home"]["name"]
        away = m["teams"]["away"]["name"]
        goals_home = m["goals"]["home"]
        goals_away = m["goals"]["away"]

        norm_home = normalize_team_name(home)
        norm_away = normalize_team_name(away)

        if norm_team == norm_home:
            result = "Win" if goals_home > goals_away else "Loss" if goals_home < goals_away else "Draw"
            opponent = away
        elif norm_team == norm_away:
            result = "Win" if goals_away > goals_home else "Loss" if goals_away < goals_home else "Draw"
            opponent = home
        else:
            if norm_team in norm_home or norm_home in norm_team:
                result = "Win" if goals_home > goals_away else "Loss" if goals_home < goals_away else "Draw"
                opponent = away
            elif norm_team in norm_away or norm_away in norm_team:
                result = "Win" if goals_away > goals_home else "Loss" if goals_away < goals_home else "Draw"
                opponent = home
            else:
                result = "Unknown"
                opponent = "Unknown"

        clean.append({
            "date": fx["date"][:10],
            "opponent": opponent,
            "home": home,
            "away": away,
            "score": f"{goals_home}-{goals_away}",
            "result": result,
        })


    return {"team": team_name, "matches": clean}