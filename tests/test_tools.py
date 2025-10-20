import requests
from config import FOOTBALL_API_KEY

url = "https://v3.football.api-sports.io/standings?league=39&season=2024"
headers = {"x-apisports-key": FOOTBALL_API_KEY}

response = requests.get(url, headers=headers)

print("Status Code:", response.status_code)
print("Response JSON:", response.json())
