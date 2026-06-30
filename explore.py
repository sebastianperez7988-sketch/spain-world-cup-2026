import requests
import matplotlib.pyplot as plt
API_KEY = "YOUR_API_KEY_HERE"  # get a free key at football-data.org

headers = {"X-Auth-Token": API_KEY}

url = "https://api.football-data.org/v4/teams/760/matches"
params = {"competitions": "WC"}

response = requests.get(url, headers=headers, params=params)
data = response.json()

opponents = []
goals_for = []
goals_against = []

for match in data['matches']:
    if match['status'] != 'FINISHED':
        continue

    home = match['homeTeam']['name']
    away = match['awayTeam']['name']
    home_score = match['score']['fullTime']['home']
    away_score = match['score']['fullTime']['away']

    if home == 'Spain':
        opponent = away
        spain_goals = home_score
        opp_goals = away_score
    else:
        opponent = home
        spain_goals = away_score
        opp_goals = home_score

    opponents.append(opponent)
    goals_for.append(spain_goals)
    goals_against.append(opp_goals)

x = range(len(opponents))

plt.figure(figsize=(8, 5))
plt.bar([i - 0.2 for i in x], goals_for, width=0.4, label='Spain', color='#AA151B')
plt.bar([i + 0.2 for i in x], goals_against, width=0.4, label='Opponent', color='#555555')

plt.xticks(x, opponents)
plt.ylabel('Goals')
plt.title("Spain's 2026 World Cup Group Stage")
plt.legend()
plt.tight_layout()
plt.savefig('spain_world_cup_2026.png')
plt.show()