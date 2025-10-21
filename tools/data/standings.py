from tools.data.utils import get_league_id, make_request

def get_league_standings(league_name="Premier League", season=2023):
    league_id = get_league_id(league_name)
    data = make_request("standings", {"league": league_id, "season": season})

    if not data or not data.get("response"):
        print(f"No standings found for {league_name} {season}.")
        return None
    
    standings = data["response"][0]["league"]["standings"][0]
    table = [
        {
            "rank": t["rank"],
            "team": t["team"]["name"],
            "points": t["points"],
            "played": t["all"]["played"],
            "wins": t["all"]["win"],
            "draws": t["all"]["draw"],
            "losses": t["all"]["lose"],
            "goals_for": t["all"]["goals"]["for"],
            "goals_against": t["all"]["goals"]["against"],

        }
        for t in standings
    ]
    return table
