import requests
from config import FOOTBALL_API_KEY

base_url = "https://v3.football.api-sports.io"

def get_premier_league_standings(season=2023):
    league_id = 39
    url = f"{base_url}/standings?league={league_id}&season={season}"
    headers = {"x-apisports-key": FOOTBALL_API_KEY}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        print("DEBUG response keys:", data.keys())


        standings = data["response"][0]["league"]["standings"][0]
        table = [
            {
                "rank": team["rank"],
                "team": team["team"]["name"],
                "points": team["points"],
                "played": team["all"]["played"],
                "wins": team["all"]["win"],
                "draws": team["all"]["draw"],
                "losses": team["all"]["lose"],
                "goals_for": team["all"]["goals"]["for"],
                "goals_against": team["all"]["goals"]["against"],
            }
            for team in standings
        ]

        return table
    except Exception as e:
        print(f"Error fetching Premier League standings: {e}")
        return None
    

def get_team_recent_matches(team_name, season=2023, last_n=5):
    headers = {"x-apisports-key": FOOTBALL_API_KEY}
    search_url = f"{base_url}/teams?search={team_name}"

    try:
        search_response = requests.get(search_url, headers=headers)
        search_response.raise_for_status()
        search_data = search_response.json()

        #print("DEBUG:", search_data)

        if not search_data["response"]:
            print(f"Team '{team_name}' not found.")
            return None
        
        team_id = search_data["response"][0]["team"]["id"]
        team_name = search_data["response"][0]["team"]["name"]

    except Exception as e:
        print(f"Error fetching team ID for {team_name}: {e}")
        return None
    
    fixtures_url = f"{base_url}/fixtures?league=39&season={season}&team={team_id}"
    try:
        fixtures_response = requests.get(fixtures_url, headers=headers)
        fixtures_response.raise_for_status()
        fixtures_data = fixtures_response.json()

        matches = fixtures_data.get("response", [])
        if not matches:
            print(f"No matches found for {team_name} in season {season}. (Free plan limitation)")
            return {"team": team_name, "matches": []}

        matches = sorted(matches, key=lambda m: m["fixture"]["date"], reverse=True)


        recent_matches = []
        for match in matches[:last_n]:
            home = match["teams"]["home"]["name"]
            away = match["teams"]["away"]["name"]
            goals_home = match["goals"]["home"]
            goals_away = match["goals"]["away"]

            if team_name == home:
                result = (
                    "Win" if goals_home > goals_away else
                    "Draw" if goals_home == goals_away else
                    "Lose"
                )
                opponent = away
            else:
                result = (
                    "Win" if goals_home < goals_away else
                    "Draw" if goals_home == goals_away else
                    "Lost"
                )
                opponent = home

            recent_matches.append({
                "date": match["fixture"]["date"][:10],
                "opponent": opponent,
                "home": home,
                "away": away,
                "score": f"{goals_home}-{goals_away}",
                "result": result
            })

        return {
                "team": team_name,
                "matches": recent_matches
        }
    except Exception as e:
        print(f"Error fetching matches for {team_name}: {e}")
        return None
    
def get_team_statistics(team_name, season=2023):
    headers = {"x-apisports-key": FOOTBALL_API_KEY}
    search_url = f"{base_url}/teams?search={team_name}"

    try:
        search_response = requests.get(search_url, headers=headers)
        search_response.raise_for_status()
        search_data = search_response.json()

        if not search_data["response"]:
            print(f"Error fetching team ID for {team_name}: {e}")
            return None
        
        team_id = search_data["response"][0]["team"]["id"]
        team_name = search_data["response"][0]["team"]["name"]
    except Exception as e:
        print(f"Error fetching team ID for {team_name}: {e}")
        return None
    
    stats_url = f"{base_url}/teams/statistics?league=39&season={season}&team={team_id}"
    try:
        stats_response = requests.get(stats_url, headers=headers)
        stats_response.raise_for_status()
        stats_data = stats_response.json()

        team_stats = stats_data.get("response", {})

        if not team_stats:
            print(f"No statistics found for {team_name} in season {season}.")
            return None
        
        summary = {
            "team": team_stats["team"]["name"],
            "league": team_stats["league"]["name"],
            "season": team_stats["league"]["season"],
            "matches_played": team_stats["fixtures"]["played"]["total"],
            "wins": team_stats["fixtures"]["wins"]["total"],
            "draws": team_stats["fixtures"]["draws"]["total"],
            "losses": team_stats["fixtures"]["loses"]["total"],
            "goals_for": team_stats["goals"]["for"]["total"]["total"],
            "goals_against": team_stats["goals"]["against"]["total"]["total"],
            "clean_sheets": team_stats["clean_sheet"]["total"],
            "failed_to_score": team_stats["failed_to_score"]["total"],
            "biggest_win": team_stats["biggest"]["wins"].get("home", None),
            "biggest_loss": team_stats["biggest"]["loses"].get("away", None),
            "average_goals_for": team_stats["goals"]["for"]["average"]["total"],
            "average_goals_against": team_stats["goals"]["against"]["average"]["total"]
        }

        return summary
    except Exception as e:
        print(f"Error fetching statistics for {team_name}: {e}")
        return None



