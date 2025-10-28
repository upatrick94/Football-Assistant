from tools.data.utils import get_league_id, make_request

def get_league_standings(league_name="Premier League", season=2023):
    league_id = get_league_id(league_name)
    data = make_request("standings", {"league": league_id, "season": season})

    if not data or not data.get("response"):
        print(f"No standings found for {league_name} {season}.")
        return None
    
    table = data["response"][0]["league"]["standings"][0]
    standings = []
    for team in table:
        standings.append({
            "position": team["rank"],
            "team": team["team"]["name"],
            "played": team["all"]["played"],
            "won": team["all"]["win"],
            "drawn": team["all"]["draw"],
            "lost": team["all"]["lose"],
            "goals_for": team["all"]["goals"]["for"],
            "goals_against": team["all"]["goals"]["against"],
            "points": team["points"],
            "form": team.get("form", "")
        })
    return standings
