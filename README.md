# Football-Assistant

**Football Assistant** is a Python app I built that combines **AI** with **live football  data**. It uses [API-FOOTBALL](https://www.api-football.com/) API to show standings, matches, stats, and more — and connects to **Google Gemini** so you can chat with it about football in real time.

---

## What It Does

- Ask football questions in natural language (thanks to Gemini)
- Get live data - standings, scorers, fixtures, stats
- Has a simple **GUI** made with PyQt6
- Uses environment variables for API Keys
- Organized code with separate modules for each feature

---

## Tools & Libraries

| Area | Technology |
|------|-------------|
| **Language** | Python 3 |
| **AI** | Google Gemini API (`google.generativeai`) |
| **Data API** | API-FOOTBALL |
| **GUI** | PyQt6 |
| **HTTP** | requests |
| **Env Config** | python-dotenv |

---

## How to Run it

### Clone the repository

- git clone 
- git clone https://github.com/yourusername/football-assistant.git
- cd football-assistant

### Create a virtual environment

- python -m venv venv
- source venv/bin/activate # (Windows: venv\Scripts\activate)

### Install packages

- pip install -r requirements.txt

### Add your API keys

Make a file named .env and put this inside:

- GEMINI_API_KEY=your_gemini_key
- FOOTBALL_API_KEY=your_football_api_key

### Run it

- python3 main.py

### Example Questions

You can ask things like:
- “Show me Premier League standings”
- “Who are the top scorers in Serie A?”   
- “How did Barcelona do in their last 5 games?”
- “When is Arsenal’s next match?”



