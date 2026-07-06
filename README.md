# Spain 2026 World Cup Analysis

Python project tracking Spain's 2026 FIFA World Cup campaign using live API data and historical StatsBomb event data.

## What's in here
- **bracket.py** — Live tournament bracket with connector lines, updates after every match
- **shot_map.py** — xG shot map from Spain vs Costa Rica (2022 World Cup, 7-0) using StatsBomb data
- **pass_network.py** — Pass network visualization showing Spain's build-up play vs Costa Rica
- **explore.py** — Original data exploration script

## Visuals
- Full 2026 World Cup bracket with results and upcoming matches
- Goals scored/conceded per match
- First half vs second half scoring breakdown
- Tournament stage progression tracker
- xG shot map with player labels and circle size scaled to chance quality
- Pass network with player positions and connection thickness scaled to pass volume

## Tools used
- Python, requests, matplotlib, mplsoccer, pandas
- football-data.org API (live 2026 data)
- StatsBomb open data (2022 historical event data)

## How to run
Get a free API key at football-data.org, add it to bracket.py, and run any script.

## Spain's 2026 run
- Group stage: Drew vs Cape Verde 0-0, beat Saudi Arabia 4-0, beat Uruguay 1-0
- Round of 32: Beat Austria 3-0
- Round of 16: Beat Portugal 1-0
- Quarter Final: July 10
