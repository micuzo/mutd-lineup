# MUTD-Lineup

This is a Twitter bot that tweets Manchester United's team lineups in a more user-friendly format. The bot retrieves game start times and lineups from [API-Football](https://www.api-football.com/) and orders the players by their positions rather than shirt numbers.

## Features

- **Automated Tweets**: The bot automatically tweets Manchester United's starting lineup, sorted by player positions.
- **Dynamic Scheduling**: The bot dynamically sets a cron job based on game start times.
- **API Integration**: Uses API-Football to retrieve match start times and lineups.

## Run
```bash
src/main.py -[lineup|mulbot]
```
```
Options:
  -lineup   update next fixture information in out.json (manually create cron job to run every day)
  -mulbot   check if lineup is out and tweet bot's reply (ran via cron job dynamically set from fixture data)
```
