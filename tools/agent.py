import re
import json

import google.generativeai as genai
from config import GEMINI_API_KEY
from tools.data.standings import get_league_standings
from tools.data.matches import get_team_recent_matches
from tools.data.stats import get_team_statistics
from tools.data.scorers import get_top_scorers
from tools.data.fixtures import get_upcoming_fixtures

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

LEAGUES = {
    "premier league": "Premier League",
    "la liga": "La Liga",
    "bundesliga": "Bundesliga",
    "serie a": "Serie A",
    "ligue 1": "Ligue 1",
}

TEAM_LEAGUE_MAP = {
    "arsenal": "Premier League",
    "manchester united": "Premier League",
    "manchester city": "Premier League",
    "liverpool": "Premier League",
    "chelsea": "Premier League",
    "tottenham": "Premier League",
    "aston villa": "Premier League",
    "newcastle": "Premier League",
    "west ham": "Premier League",


    "real madrid": "La Liga",
    "barcelona": "La Liga",
    "atletico madrid": "La Liga",
    "sevilla": "La Liga",
    "real sociedad": "La Liga",
    "valencia": "La Liga",


    "bayern munich": "Bundesliga",
    "borussia dortmund": "Bundesliga",
    "rb leipzig": "Bundesliga",
    "bayer leverkusen": "Bundesliga",
    "vfb stuttgart": "Bundesliga",
    "eintracht frankfurt": "Bundesliga",
    "hoffenheim": "Bundesliga",


    "inter": "Serie A",
    "ac milan": "Serie A",
    "juventus": "Serie A",
    "napoli": "Serie A",
    "roma": "Serie A",
    "lazio": "Serie A",


    "psg": "Ligue 1",
    "paris saint germain": "Ligue 1",
    "marseille": "Ligue 1",
    "lyon": "Ligue 1",
    "monaco": "Ligue 1",
}


def detect_league(text: str):
    for k, v in LEAGUES.items():
        if k in text.lower():
            return v
    return "Premier League"

def detect_team(text: str):
    clean_text = text.lower()
    clean_text = re.sub(r"[’']s\b", "", clean_text)
    clean_text = re.sub(r"[^a-z0-9\s]", "", clean_text)

    aliases = {
        "arsenal": "Arsenal",
        "manchester united": "Manchester United",
        "man united": "Manchester United",
        "man utd": "Manchester United",
        "united": "Manchester United",
        "manchester city": "Manchester City",
        "man city": "Manchester City",
        "city": "Manchester City",
        "liverpool": "Liverpool",
        "chelsea": "Chelsea",
        "spurs": "Tottenham",
        "tottenham": "Tottenham",

        "real madrid": "Real Madrid",
        "real": "Real Madrid",
        "madrid": "Real Madrid",
        "barcelona": "Barcelona",
        "barca": "Barcelona",
        "atletico": "Atletico Madrid",
        "atletico madrid": "Atletico Madrid",

        "bayern": "Bayern Munich",
        "bayern munich": "Bayern Munich",
        "munich": "Bayern Munich",
        "dortmund": "Borussia Dortmund",
        "leipzig": "RB Leipzig",
        "leverkusen": "Bayer Leverkusen",

        "inter": "Inter",
        "inter milan": "Inter",
        "milan": "AC Milan",
        "ac milan": "AC Milan",
        "juventus": "Juventus",
        "juve": "Juventus",
        "napoli": "Napoli",
        "roma": "Roma",

        "psg": "PSG",
        "paris": "PSG",
        "paris saint germain": "PSG",
        "marseille": "Marseille",
    }

    for key, full_name in aliases.items():
        if key in clean_text.split() or key in clean_text:
            return full_name

    return None


def detect_intent(text: str):
    t = text.lower()
    if any(k in t for k in ["top scorer", "goals", "golden boot"]):
        return "scorers"
    if any(k in t for k in ["standings", "table", "ranking", "positions"]):
        return "standings"
    if any(k in t for k in ["stat", "performance", "record"]):
        return "stats"
    if any(k in t for k in ["next match", "upcoming", "fixtures", "schedule"]):
        return "fixtures"
    if any(k in t for k in ["recent", "last", "results", "form", "matches"]):
        return "recent"
    return "unknown"

def parse_prompt_with_gemini(prompt: str):
    prompt = re.sub(r"([A-Za-z]+)'s", r"\1", prompt)
    instruction = f"""
    You are a football data assistant. Read the following user request and extract:
    - intent: one of ["scorers", "standings", "fixtures", "recent", "stats"]
    - team: (if a specific club is mentioned)
    - league: (if a league is mentioned)

    Return valid JSON, for example:
    {{"intent": "recent", "team": "Bayern Munich", "league": "Bundesliga"}}

    USER MESSAGE:
    \"\"\"{prompt}\"\"\"
    """
    try:
        response = model.generate_content(instruction)
        text = response.text.strip()
        parsed = json.loads(text)
        return {
            "intent": parsed.get("intent", "unknown"),
            "team": parsed.get("team"),
            "league": parsed.get("league"),
        }
    except Exception:
        return {"intent": "unknown", "team": None, "league": None}


def football_agent(prompt: str, season=2023):
    intent = detect_intent(prompt)
    team = detect_team(prompt)
    league = detect_league(prompt)

    if (intent == "unknown" or not team) and len(prompt.split()) > 2:
        parsed = parse_prompt_with_gemini(prompt)
        intent = parsed["intent"] if parsed["intent"] != "unknown" else intent
        league = parsed["league"] or league
        team = parsed["team"] or team

    if team and (league == "Premier League" or not league):
        team_key = team.lower()
        if team_key in TEAM_LEAGUE_MAP:
            league = TEAM_LEAGUE_MAP[team_key]

    try:
        if intent == "scorers":
            data = get_top_scorers(league, season)
            if not data:
                return f"Couldn't get top scorers for {league}."
            lines = [f"🏆 Top scorers in {league} {season}/{season+1}:"]
            for i, s in enumerate(data, 1):
                lines.append(f"{i}. {s['player']} ({s['team']}) – {s['goals']} G, {s['assists']} A")
            return "\n".join(lines)

        if intent == "standings":
            data = get_league_standings(league, season)
            if not data:
                return f"Couldn't get standings for {league}."
            lines = [f"📊 {league} Standings {season}/{season+1}:"]
            for t in data[:10]:
                lines.append(f"{t['position']}. {t['team']} - {t['points']} pts ({t['won']}W {t['drawn']}D {t['lost']}L)")
            return "\n".join(lines)

        if intent == "fixtures":
            if not team:
                return "Please specify a team to check upcoming fixtures."
            data = get_upcoming_fixtures(team, league, season)
            if not data:
                return f"No fixtures found for {team}."
            lines = [f"📅 {team} upcoming fixtures ({league} {season}/{season+1}):"]
            for f in data["fixtures"][:5]:
                lines.append(f"{f['date']}: {f['home']} vs {f['away']} at {f['venue']} [{f['match_status']}]")
            return "\n".join(lines)

        if intent == "recent":
            if not team:
                return "Please specify a team to check recent matches."
            data = get_team_recent_matches(team, league, season)
            if not data:
                return f"No recent matches found for {team}."
            lines = [f"🕓 {team} recent matches ({league} {season}/{season+1}):"]
            for m in data["matches"]:
                lines.append(f"{m['date']}: {m['home']} {m['score']} {m['away']} ({m['result']})")
            return "\n".join(lines)

        if intent == "stats":
            if not team:
                return "Please specify a team to check statistics."
            data = get_team_statistics(team, league, season)
            if not data:
                return f"No statistics found for {team}."
            return (
                f"📈 {team} in {league} ({season}/{season+1}): "
                f"{data['wins']}W-{data['draws']}D-{data['losses']}L, "
                f"{data['goals_for']} GF / {data['goals_against']} GA"
            )

        return "🤔 Sorry, I couldn't understand your request. Try asking about standings, top scorers, fixtures, or recent matches."

    except Exception as e:
        return f"⚠️ Data retrieval error: {e}"


class FootballAgent:
    def __init__(self, season: int = 2023):
        self.season = season

    def ask(self, query: str) -> str:
        try:
            from tools.agent import football_agent
            return football_agent(query, self.season)
        except Exception as e:
            return f"⚠️ Error while processing request: {e}"

