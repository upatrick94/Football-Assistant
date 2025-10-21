from tools.data.utils import make_request, get_league_id

def get_top_scorers(league_name="Premier League", season=2023, limit=10):
    league_id = get_league_id(league_name)
    data = make_request("players/topscorers", {"league": league_id, "season": season})
    if not data or not data.get("response"):
        print(f"No top scorers found for {league_name}.")
        return None
    
    scorers = data["response"][:limit]
    top = [
        {
            "player": s["player"]["name"],
            "team": s["statistics"][0]["team"]["name"],
            "goals": s["statistics"][0]["goals"]["total"],
            "assists": s["statistics"][0]["goals"]["assists"],
        }
        for s in scorers
    ]

    return top