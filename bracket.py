import requests

API_KEY = "705a3bbaa05643979f0ea5ea3baf5dc2"
headers = {"X-Auth-Token": API_KEY}

url = "https://api.football-data.org/v4/competitions/WC/matches"
response = requests.get(url, headers=headers)
data = response.json()

r16 = [m for m in data['matches'] if m['stage'] == 'LAST_16']
for m in r16:
    home = m['homeTeam']['name']
    away = m['awayTeam']['name']
    print(f"{home} vs {away} - {m['status']} - {m['utcDate'][:10]}")