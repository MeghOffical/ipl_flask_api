from flask import Flask, jsonify, request
import ipl

app = Flask(__name__)

# Home route
@app.route('/')
def index():
    return "I am Megh Bavarva. This is own created API."


# Get all team names
@app.route('/api/teams')
def teams():
    return jsonify(ipl.team_name())


# Head-to-head stats between two teams
@app.route('/api/teamVteam')
def teamVteam():
    team1 = request.args.get('team1')
    team2 = request.args.get('team2')
    return jsonify(ipl.team_vs_team(team1, team2))


# All teams and their win count
@app.route('/api/team_winning_record')
def team_winning_record():
    return jsonify(ipl.winning_team())


# Most appearances in IPL finals
@app.route('/api/most_final_played')
def most_final_played():
    return jsonify(ipl.most_final_played())


# Get list of all bowlers
@app.route('/api/name_of_bowlers')
def bowlers():
    return jsonify({"bowler": ipl.no_of_bowler()})


# Get list of all batsmen
@app.route('/api/name_of_batsmens')
def batsman():
    return jsonify({"batsmen": ipl.no_of_batsman()})


# Detailed stats for a specific bowler
@app.route('/api/bowler_details')
def bowler_details_api():
    bowler = request.args.get('bowler')
    return jsonify(ipl.bowler_details(bowler))


# Detailed stats for a specific batsman
@app.route('/api/batsman_details')
def batsman_details_api():
    batsman = request.args.get('batsman')
    return jsonify(ipl.batsman_details(batsman))


# Top wicket-taker (Purple Cap)
@app.route('/api/purple_cap')
def purple_cap():
    return jsonify(ipl.purple_cap())


# Top run-scorer (Orange Cap)
@app.route('/api/orange_cap')
def orange_cap():
    return jsonify(ipl.orange_cap())


# Point table with rankings and positions
@app.route('/api/point_table')
def point_table():
    season = request.args.get('season')
    return jsonify(ipl.point_table_extension(season))


# Player of the match details
@app.route('/api/Player_Of_Match')
def player_of_match():
    return jsonify(ipl.Player_Of_match_details())


# Top batting partnerships
@app.route('/api/batting_pair')
def batting_pair():
    return jsonify(ipl.batting_pair())


# Run the Flask app
# if __name__ == '__main__':
#     app.run(debug=True)
