from tools.data.utils import get_league_id, make_request, resolve_team_id

def get_team_statistics(team_name, league_name="Premier League", season=2023):
    league_id = get_league_id(league_name)
    team_id, resolve_name = resolve_team_id(team_name, league_id, season)
    if not team_id:
        print(f"Team '{team_name} not found.'")

    stats_data = make_request("teams/statistics", {"league": league_id, "season": season, "team": team_id})
    if not stats_data or not stats_data.get("response"):
        print(f"No statistics available for {team_name} in {league_name}.")
        return None
    stats = stats_data["response"]
    summary = {
        "team": team_name,
        "league": league_name,
        "played": stats["fixtures"]["played"]["total"],
        "wins": stats["fixtures"]["wins"]["total"],
        "draws": stats["fixtures"]["draws"]["total"],
        "losses": stats["fixtures"]["loses"]["total"],
        "goals_for": stats["goals"]["for"]["total"],
        "goals_against": stats["goals"]["against"]["total"],
        "clean_sheets": stats["clean_sheet"]["total"],
        "failed_to_score": stats["failed_to_score"]["total"],
        "biggest_win": stats["biggest"]["wins"]["home"] or stats["biggest"]["wins"]["away"],

    }
    return summary
