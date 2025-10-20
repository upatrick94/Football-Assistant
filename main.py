from tools.football_data import get_team_statistics

stats = get_team_statistics("Arsenal")
if stats:
    print("\n=== Team Statistics ===")
    for k, v in stats.items():
        print(f"{k}: {v}")
