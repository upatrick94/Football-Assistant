import google.generativeai as genai
from config import GEMINI_API_KEY
from tools.football_data import(
    get_premier_league_standings,
    get_team_recent_matches,
    get_team_statistics,
    get_top_scorers,
    get_upcoming_fixtures
)

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

def football_agent(prompt):
    prompt_lower = prompt.lower()

    if "standing" in prompt_lower or "table" in prompt_lower:
        data = get_premier_league_standings()
        if not data:
            return "Sorry, I couldn't fetch the league standings."
        return model.generate_content(f"Summarize this Premier League table briefly:\n{data}").text
    elif "stat" in prompt_lower or "performance" in prompt_lower:
        team = extract_team_name(prompt)
        data = get_team_statistics(team)
        if not data:
            return f"Sorry, I couldn't fetch statistics for {team}."
        return model.generate_content(f"Write a short analysis of {team}'s performance this season using this data:\n{data}").text
    elif "recent" in prompt_lower or "scorer" in prompt_lower:
        team = extract_team_name(prompt)
        data = get_team_recent_matches(team)
        if not data:
            return f"Sorry, I couldn’t fetch recent matches for {team}."
        return model.generate_content(f"Summarize {team}'s recent matches:\n{data}").text
    elif "top" in prompt_lower or "scorer" in prompt_lower:
        data = get_top_scorers()
        if not data:
            return "Sorry, I couldn’t fetch the top scorers."
        return model.generate_content(f"Summarize the top goal scorers in the Premier League:\n{data}").text
    elif "next" in prompt_lower or "upcoming" in prompt_lower or "fixture" in prompt_lower:
        team = extract_team_name(prompt)
        data = get_team_recent_matches(team)
        if not data:
            return f"Sorry, I couldn’t fetch upcoming fixtures for {team}."
        return model.generate_content(f"Summarize {team}'s next fixtures:\n{data}").text
    else:
        return model.generate_content(f"You are a football data assistant. Answer this:\n{prompt}").text

def extract_team_name(prompt):
    teams = ["Arsenal", "Manchester United", "Chelsea", "Liverpool", "Tottenham", "Manchester City"]
    for team in teams:
        if team.lower() in prompt.lower():
            return team
    return "Arsenal"