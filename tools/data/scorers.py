from tools.data.utils import make_request, get_league_id

def get_top_scorers(league_name="Premier League", season=2023, limit=10):
    league_id = get_league_id(league_name)

    data = make_request("players/topscorers", {"league": league_id, "season": season})
    if not data or not data.get("response"):
        print(f"No scorer data found for {league_name} ({season}).")
        return None

    scorers = []
    for p in data["response"][:limit]:
        player_name = p.get("player", {}).get("name", "Unknown Player")

        stats = p.get("statistics", [{}])[0]
        team_name = stats.get("team", {}).get("name", "Unknown Team")

        goals = stats.get("goals", {}).get("total", 0) or 0
        assists = stats.get("goals", {}).get("assists", 0) or 0

        scorers.append({
            "player": player_name,
            "team": team_name,
            "goals": goals,
            "assists": assists
        })

    return scorers