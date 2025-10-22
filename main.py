from tools.data.scorers import get_top_scorers
from tools.data.matches import get_team_recent_matches
from tools.data.fixtures import get_upcoming_fixtures

print("Top scorers in Bundesliga:")
print(get_top_scorers("Bundesliga"))

print("\nArsenal upcoming fixtures:")
print(get_upcoming_fixtures("Arsenal", "Premier League"))

print("\nBayern recent matches:")
print(get_team_recent_matches("Borussia Dortmund", "Bundesliga"))
