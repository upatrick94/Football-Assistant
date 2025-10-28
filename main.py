from tools.data.scorers import get_top_scorers
from tools.data.matches import get_team_recent_matches
from tools.data.fixtures import get_upcoming_fixtures

def print_scorers(league="Bundesliga", season=2023):
    print(f"Top scorers in {league} {season}/{season+1}:")
    data = get_top_scorers(league, season)
    if not data:
        print("No data.")
        return
    for i, s in enumerate(data, 1):
        print(f"{i}. {s['player']} ({s['team']}) – {s['goals']} G, {s.get('assists') or 0} A")

def print_upcoming(team="Arsenal", league="Premier League", season=2023):
    print(f"\n{team} upcoming fixtures ({league} {season}/{season+1}):")
    data = get_upcoming_fixtures(team, league, season)
    if not data:
        print("No data.")
        return
    for f in data["fixtures"]:
        print(f"{f['date']}: {f['home']} vs {f['away']} at {f['venue']} [{f['match_status']}]")

def print_recent(team="Bayern Munich", league="Bundesliga", season=2023):
    print(f"\n{team} recent matches ({league} {season}/{season+1}):")
    data = get_team_recent_matches(team, league, season)
    if not data:
        print("No data.")
        return
    for m in data["matches"]:
        print(f"{m['date']}: {m['home']} {m['score']} {m['away']}  ({m['result']})")

if __name__ == "__main__":
    print_scorers("Bundesliga", 2023)
    print_upcoming("Arsenal", "Premier League", 2023)
    print_recent("Bayern Munich", "Bundesliga", 2023)
