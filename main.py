from tools.football_data import get_team_recent_matches

result = get_team_recent_matches("Manchester United")
if result:
    print(f"Last {len(result['matches'])} matches for {result['team']}:")
    for m in result["matches"]:
        print(f"{m['date']}: {m['home']} {m['score']} {m['away']} ({m['result']})")
