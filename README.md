IPL Flask API

A RESTful API built with Flask to serve comprehensive IPL (Indian Premier League) statistics from 2008 to 2022. This project demonstrates clean architecture, efficient data processing with Pandas, and deployment-ready configurations.

🔍 Key Features

Team Endpoints: Retrieve list of all IPL teams.

Head-to-Head: Compare two teams' performance against each other.

Winning Records: Overall winning percentages and most finals played.

Player Statistics: Season-wise batsman and bowler details.

Caps: Purple Cap (most wickets) and Orange Cap (most runs) winners.

Point Table: Standings by season with Net Run Rate (NRR).

Partnerships & Player of the Match: Top batting pairs and standout players.

📁 Project Structure

ipl_flask_api/
├── data/
│   ├── IPL_Matches_2008_2022.csv    # Match-level data
│   ├── IPL_Ball_by_Ball_2008_2022.csv  # Ball-by-ball data
│   └── ipl_deliveries.csv            # Cleaned deliveries dataset
├── Testing.ipynb                    # Exploratory data analysis & prototyping
├── backend.py                       # Flask application & route definitions
├── ipl.py                           # Data loading and processing functions
├── requirements.txt                 # Python dependencies
└── Procfile                         # Deployment config for Render.com

⚙️ Prerequisites

Python 3.7+

pip

🚀 Installation & Setup

Clone the repository

git clone https://github.com/MeghOffical/ipl_flask_api.git
cd ipl_flask_api

Install dependencies

pip install -r requirements.txt

Run locally

export FLASK_APP=backend.py
flask run

Deploy on Render

Create a new Web Service on Render.

Connect your GitHub repo.

Use the included Procfile (web: gunicorn backend:app).

🔗 API Reference

Endpoint

Method

Query Params

Description

/

GET

—

Welcome message

/api/teams

GET

—

List of all IPL teams

/api/teamVteam

GET

team1, team2

Head-to-head stats

/api/team_winning_record

GET

—

Winning percentages for each team

/api/most_final_played

GET

—

Players with most finals appearances

/api/name_of_bowlers

GET

—

List of all bowlers

/api/name_of_batsmens

GET

—

List of all batsmen

/api/bowler_details

GET

bowler

Season-wise stats for a specific bowler

/api/batsman_details

GET

batsman

Season-wise stats for a specific batsman

/api/purple_cap

GET

—

Purple Cap winners (highest wickets per season)

/api/orange_cap

GET

—

Orange Cap winners (highest runs per season)

/api/point_table

GET

season (e.g. 2023)

Points table with NRR for specified season

/api/Player_Of_Match

GET

—

Player of the match counts

/api/batting_pair

GET

—

Top batting partnerships by cumulative runs

🛠️ Under the Hood

Data Loading: Uses Pandas to read CSVs.
Normalization: Standardizes team names via mapping.
Merging: Combines match and ball-level data for advanced metrics.
Feature Engineering:
Flags for legal deliveries and bowler dismissals.
Excludes extras like byes and leg-byes from bowler runs.
Stat Functions: GroupBy operations to compute per-season and overall statistics.


🎯 Talking Points

Modular Design: Separation of backend.py (API layer) and ipl.py (analytics layer).
Pandas Expertise: Efficient use of groupby, merge, and custom flags on ~300K rows.
Scalability: Discuss caching, pagination, or database-backed enhancements.
Deployment: Zero-downtime free hosting with Render and Gunicorn.


📄 License

This project is open-source.


For questions or feedback, feel free to open an issue or submit a pull request!
