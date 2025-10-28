from tools.data.utils import resolve_team_id, get_league_id

league_id = get_league_id("Bundesliga")
tid, name = resolve_team_id("Bayern Munich", league_id, 2023)
print(tid, name)