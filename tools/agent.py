import google.generativeai as genai
from config import GEMINI_API_KEY
from data.standings import get_league_standings
from data.matches import get_team_recent_matches
from data.stats import get_team_statistics
from data.scorers import get_top_scorers
from data.fixtures import get_upcoming_fixtures
from data.utils import get_league_id

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

DEFAULT_LEAGUE = "Premier League"
DEFAULT_SEASON = 2023

def _league_from_prompt(p: str) -> str:
    p = p.lower()
    if "la liga" in p: return "La Liga"
    if "serie a" in p: return "Serie A"
    if "bundesliga" in p: return "Bundesliga"
    if "ligue 1" in p or "ligue1" in p: return "Ligue 1"
    return DEFAULT_LEAGUE

def _team_from_prompt(p: str) -> str:
    teams = ["Arsenal","Manchester United","Chelsea","Liverpool","Tottenham",
             "Manchester City","FC Bayern München","Bayern Munich","Real Madrid",
             "Barcelona","Inter","AC Milan","Juventus","PSG","RB Leipzig","Borussia Dortmund"]
    p_low = p.lower()
    for t in teams:
        if t.lower() in p_low:
            return t
    return "Arsenal"

def football_agent(prompt: str):
    p = prompt.lower()
    league = _league_from_prompt(prompt)
    season = DEFAULT_SEASON

    if "standing" in p or "table" in p:
        data = get_league_standings(league, season)
        if not data:
            return "Sorry, I couldn't fetch league standings."
        return model.generate_content(f"Summarize {league} {season}/{season+1} table briefly:\n{data}").text

    if "stat" in p or "performance" in p:
        team = _team_from_prompt(prompt)
        data = get_team_statistics(team, league, season)
        if not data:
            return f"Sorry, I couldn't fetch statistics for {team}."
        return model.generate_content(f"Write a short analysis of {team}'s season using this data:\n{data}").text

    if "recent" in p or "last" in p or "form" in p:
        team = _team_from_prompt(prompt)
        data = get_team_recent_matches(team, league, season, last_n=5)
        if not data:
            return f"Sorry, I couldn't fetch recent matches for {team}."
        return model.generate_content(f"Summarize {team}'s last 5 matches:\n{data}").text

    if "next" in p or "upcoming" in p or "fixture" in p or "schedule" in p:
        team = _team_from_prompt(prompt)
        data = get_upcoming_fixtures(team, league, season, limit=5)
        if not data:
            return f"Sorry, I couldn’t fetch upcoming fixtures for {team}."
        return model.generate_content(f"Summarize {team}'s next fixtures:\n{data}").text

    if "top scorer" in p or "scorer" in p or "golden boot" in p:
        data = get_top_scorers(league, season, limit=10)
        if not data:
            return f"Sorry, I couldn't fetch top scorers for {league}."
        return model.generate_content(f"Give a concise take on {league} top scorers {season}/{season+1}:\n{data}").text

    return model.generate_content(f"You are a football data assistant. Answer this:\n{prompt}").text
