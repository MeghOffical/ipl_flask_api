import numpy as np
import pandas as pd

# Load the data set 
ipl=pd.read_csv("C:\\Users\\MEGH BAVARVA\\Desktop\\Data Scientist\\Project\\API_development\\Code\\IPL_Matches_2008_2022.csv")
balls=pd.read_csv("C:\\Users\\MEGH BAVARVA\\Desktop\\Data Scientist\\Project\\API_development\\Code\\IPL_Ball_by_Ball_2008_2022.csv")
deliveries=pd.read_csv("C:\\Users\\MEGH BAVARVA\\Desktop\\Data Scientist\\Project\\API_development\\Code\\ipl_deliveries.csv")


# change neccesaary thing in data sets



# chnage team name 
change_team={
    'Delhi Daredevils':'Delhi Capitals',
    'Kings XI Punjab ':'Punjab Kings',
    'Rising Pune Supergiants ':'Rising Pune Supergiant'
}
ipl.replace(change_team.keys(),change_team.values(),inplace=True) 

# Merge 'balls' and 'ipl' data on match ID to get season-wise ball data
season = balls.merge(ipl[['ID', 'Season']], how='inner', on='ID')

# Add a new column marking only genuine bowler wickets (exclude run-outs etc.)
season['IsBowlerWicket'] = season['kind'].apply(
    lambda x: 1 if x in ('caught', 'caught and bowled', 'bowled', 'stumped','lbw', 'hit wicket') else 0
)

# Count runs given by bowler (exclude legbyes/byes as they’re not bowler’s fault)
season['Bowler_run'] = season['extra_type'].apply(
    lambda x: 0 if x in ('legbyes','byes') else 1
) * season['total_run']


# Identify legal deliveries (exclude wides and no-balls)
season['LegalDilevery'] = season['extra_type'].apply(
    lambda x: 0 if x in ('wides','noballs') else 1
)

# Mark player dismissed only if batter == player_out
season['Player_out_hai'] = ((season['isWicketDelivery'] == 1) & (season['batter'] == season['player_out'])).astype(int)



# Functions used  to fecth the required data 



def team_name():
    
    # Get all unique team names from both Team1 and Team2 columns
    team1 = ipl['Team1'].unique()
    team2 = ipl['Team2'].unique()

    # Combine and remove duplicates to get all valid team names
    all_teams = pd.unique(np.concatenate((team1, team2)))
    
    team_dict ={
        "teams": list(all_teams)
    }

    return team_dict




def team_vs_team(team1, team2):
    
    # Get all unique team names from both Team1 and Team2 columns
    team1_ = ipl['Team1'].unique()
    team2_ = ipl['Team2'].unique()

    # Combine and remove duplicates to get all valid team names
    valid_team = pd.unique(np.concatenate((team1_, team2_)))

    # Check if both input teams are valid
    if ((team1 in valid_team) and (team2 in valid_team)):

        # Get all matches played between team1 and team2 (any order)
        match = ipl[((ipl['Team1'] == team1) & (ipl['Team2'] == team2)) |
                    ((ipl['Team1'] == team2) & (ipl['Team2'] == team1))]

        # Total number of matches played
        no_of_match = match.shape[0]

        # Count how many matches team1 won
        team1_win = match[match['WinningTeam'] == team1].shape[0]

        # Count how many matches team2 won
        team2_win = match[match['WinningTeam'] == team2].shape[0]

        # Remaining matches are considered draws or no result
        draws = no_of_match - (team1_win + team2_win)

        # Calculate win percentage for both teams (rounded to 2 decimal places)
        team1_win_percentage = round((team1_win / no_of_match) * 100, 2)
        team2_win_percentage = round((team2_win / no_of_match) * 100, 2)

       
        team_vs_team_dict = {
            "team1": team1,
            "team2": team2,
            "matches_played": no_of_match,
            "team1_win": team1_win,
            "team1_win_percentage": round(team1_win_percentage, 2),
            "team2_win": team2_win,
            "team2_win_percentage": round(team2_win_percentage, 2),
            "draws": draws
        }

        
        return team_vs_team_dict

    else:
        # If team names are not valid, return error message
        return 
        {
            "error": "Invalid team names provided. Please check the team names."
        }





def winning_team():
    
    # Remove rows where WinningTeam is null (missing)
    df = ipl[~ipl['WinningTeam'].isnull()]

    # Get all unique teams from both Team1 and Team2 columns
    team_1 = df['Team1'].unique()
    team_2 = df['Team2'].unique()

    # Get all unique team names (union of both lists)
    total_team = np.union1d(team_1, team_2)

    # This list will store the result for each team
    data_list = []

  
    for team in total_team:
        # All matches played by the team (as Team1 or Team2)
        total_matches = df[(df['Team1'] == team) | (df['Team2'] == team)]

        # Matches where this team won
        total_wins = total_matches[total_matches['WinningTeam'] == team]

        # Matches won at home 
        home_wins = total_matches[(total_matches['WinningTeam'] == team) & (total_matches['Team1'] == team)]

        # Matches won away
        away_wins = total_matches[(total_matches['WinningTeam'] == team) & (total_matches['Team2'] == team)]

        # Calculate percentages (with 0 division check)
        wins_perc = (total_wins.shape[0] / total_matches.shape[0]) * 100 if total_matches.shape[0] > 0 else 0
        home_wins_perc = (home_wins.shape[0] / total_wins.shape[0]) * 100 if total_wins.shape[0] > 0 else 0
        away_wins_perc = (away_wins.shape[0] / total_wins.shape[0]) * 100 if total_wins.shape[0] > 0 else 0

        
        data_list.append([
            team,
            total_matches.shape[0],
            round(wins_perc, 2),
            round(home_wins_perc, 2),
            round(away_wins_perc, 2)
        ])

    # Create DataFrame from result
    result_df = pd.DataFrame(
        data_list,
        columns=["Team", "Matches_Played", "Win_Percentage", "Home_Wins_Percentage", "Away_Wins_Percentage"]
    )

    # Sort by win percentage (highest first)
    result_df = result_df.sort_values("Win_Percentage", ascending=False).reset_index(drop=True)

    # Convert to dictionary and return
    return result_df.to_dict(orient='records')





# Helper function 
def getplayer(l):
    # Remove brackets and split by comma, then clean each name
    return pd.Series([p.strip().strip("'") for p in l.strip("[]").split(",")])


def most_final_played():
    # Filter the DataFrame to get only the rows where match is Final
    final_match = ipl[ipl['MatchNumber'] == 'Final']

    # List to store all player names who played in finals
    players_list = []

    # Add players from Team1Players column
    for player in final_match['Team1Players']:
        players_list.extend(getplayer(player))

    # Add players from Team2Players column
    for player in final_match['Team2Players']:
        players_list.extend(getplayer(player))

    # Convert the list into a Series
    big_player = pd.Series(players_list)

    # Get top 10 players who appeared most in finals
    ans = big_player.value_counts().head(10)

    # Return the result as dictionary
    return ans.to_dict()





def no_of_bowler(): 
    return season['bowler'].unique().tolist()



def no_of_batsman():
    return season['batter'].unique().tolist()




def bowler_details(player_name):
    # Filter rows where player was the bowler
    player = season[season['bowler'] == player_name]
    
    # 1. Total innings bowled (unique matches)
    innings_bowled = player.groupby(['Season'])['ID'].nunique()
    col1 = innings_bowled.reset_index(name="Innings")

    # 2. Total wickets taken (only valid bowler dismissals)
    total_wickets = player[player['IsBowlerWicket'] == 1].groupby(['Season'])['IsBowlerWicket'].sum()
    col2 = total_wickets.reset_index(name="Wickets")

    # 3. Best spell (most wickets in a match per season)
    best_spell = player[player['IsBowlerWicket'] == 1].groupby(['Season', 'ID'])['IsBowlerWicket'].sum().reset_index()
    best_spell = best_spell.sort_values(by=['Season', 'IsBowlerWicket'], ascending=[True, False])
    best_spell = best_spell.drop_duplicates(subset=['Season'], keep='first')
    col3 = best_spell[['Season', 'IsBowlerWicket']].rename(columns={'IsBowlerWicket': 'Best_spell'})

    # 4. Total runs conceded by bowler
    runs_conceded = player.groupby(['Season'])['Bowler_run'].sum()
    col4 = runs_conceded.reset_index(name="Runs_conceded")

    # 5. Legal deliveries bowled
    legal_balls = player[player['LegalDilevery'] == 1].groupby(['Season'])['ballnumber'].count()
    col5 = legal_balls.reset_index(name="Balls_bowled")

    # 6. Economy rate = (runs / balls) * 6
    economy_rate = round((runs_conceded / legal_balls.replace(0, np.nan)) * 6, 2)
    col6 = economy_rate.reset_index(name="Economy")

    # Merge all the stats into one DataFrame
    stats = col1.merge(col2, on='Season', how='left') \
                .merge(col3, on='Season', how='left') \
                .merge(col4, on='Season', how='left') \
                .merge(col5, on='Season', how='left') \
                .merge(col6, on='Season', how='left')

    stats.fillna(0, inplace=True)

    # Return important columns as a list of dictionaries
    return stats[['Season', 'Innings', 'Wickets', 'Best_spell', 'Runs_conceded', 'Economy']].to_dict(orient='records')




def batsman_details(player_name):     
    # Filter rows where player was the batter
    player = season[season['batter'] == player_name]

    # 1. Total innings played
    innings_played = player.groupby(['Season'])['ID'].nunique()
    col1 = innings_played.reset_index(name="innings_played")

    # 2. Total runs scored
    batsman_runs = player.groupby(['Season'])['total_run'].sum()
    col2 = batsman_runs.reset_index(name="Total_runs")

    # 3. Total times dismissed
    batsman_out = season[season['player_out'] == player_name]
    req = batsman_out.groupby('Season')['isWicketDelivery'].sum()
    col3 = req.reset_index(name="total_no_out")

    # 4. Batting average = total runs / outs
    Average = batsman_runs / req
    col4 = Average.reset_index(name="average")

    # 5. Highest runs in a single match per season
    highest_runs = player.groupby(['Season','ID'])['batsman_run'].sum().reset_index()
    highest_runs = highest_runs.sort_values(by=['batsman_run'],ascending=False).drop_duplicates(subset=['Season'],keep='first')
    highest_runs = highest_runs.set_index('Season').sort_index()
    col5 = highest_runs.reset_index()[['Season','batsman_run']]

    # 6. Total balls played (excluding wides)
    balls_not_wide = player[~(player["extra_type"] == 'wides')]
    batsman_balls = balls_not_wide.groupby(['Season'])['ballnumber'].count()
    col6 = batsman_balls.reset_index(name="Ball_played")

    # 7. Strike rate = (runs / balls) * 100
    strike_rate = round((batsman_runs / batsman_balls) * 100, 2)
    col7 = strike_rate.reset_index(name='StrikeRate')

    # Merge all into one DataFrame
    stats = col1.merge(col2,on='Season') \
                .merge(col3,on='Season') \
                .merge(col4,on='Season') \
                .merge(col5,on='Season') \
                .merge(col6,on='Season') \
                .merge(col7,on='Season')

    # Rename for clean output
    stats.rename(columns={
        'innings_played': "Innings",
        'average': 'Average',
        'batsman_run': 'Highest_runs',
        'StrikeRate': 'Strike_rate'
    }, inplace=True)

    # Return relevant columns as dictionary
    return stats[['Season','Innings','Total_runs','Average','Highest_runs','Strike_rate']].to_dict(orient='index')

    


def purple_cap():
    # Group by Season and Bowler, calculate total wickets, runs, and legal deliveries
    pcapdf = season.groupby(['Season', 'bowler']).agg({
        'IsBowlerWicket': 'sum',
        'Bowler_run': 'sum',
        'LegalDilevery': 'sum',
    })

    # Calculate economy rate = (runs / balls) * 6
    pcapdf['Bowler_Economy'] = round((pcapdf['Bowler_run'] / pcapdf['LegalDilevery']) * 6, 2)

    # Reset index and sort by wickets (desc) and economy (asc) to break ties
    final = pcapdf.reset_index().sort_values(
        by=['IsBowlerWicket', 'Bowler_Economy'],
        ascending=[False, True]
    )

    # Pick top bowler for each season
    final = final.drop_duplicates(subset=['Season'], keep='first').sort_values('Season').set_index('Season')

    # Rename columns for final output
    final = final[['bowler', 'IsBowlerWicket', 'Bowler_Economy']].rename(columns={
        'bowler': 'Best_Bowler',
        'IsBowlerWicket': 'Wickets',
        'Bowler_Economy': 'Economy'
    })

    return final.to_dict(orient='index')


def orange_cap():

    # Group by Season and Batsman to calculate runs, outs, balls
    temp = season.groupby(['Season', 'batter']).agg({
        'batsman_run': 'sum',
        'LegalDilevery': 'sum',
        'Player_out_hai': 'sum'
    }).reset_index()

    # Average = runs / outs (if out == 0, assign full runs as average)
    temp['Average'] = temp['batsman_run'] / temp['Player_out_hai']
    temp['Average'] = temp.apply(
        lambda row: row['batsman_run'] if row['Player_out_hai'] == 0 else round(row['Average'], 2),
        axis=1
    )

    # Strike Rate = (runs / balls) * 100
    temp['Strike_Rate'] = round((temp['batsman_run'] / temp['LegalDilevery']) * 100, 2)

    # Sort by runs > strike rate > average to break ties
    temp.sort_values(by=['batsman_run', 'Strike_Rate', 'Average'], ascending=[False, False, False], inplace=True)

    # Keep top batsman per season
    temp.drop_duplicates(subset=['Season'], keep='first', inplace=True)

    # Set index and rename columns
    final = temp.sort_values('Season').set_index('Season')[['batter', 'batsman_run', 'Strike_Rate', 'Average']].rename(columns={
        'batter': 'Batsman',
        'batsman_run': 'Runs'
    })

    return final.to_dict(orient='index')





def matched_played(df, team):
    return df[(df['Team1'] == team) | (df['Team2'] == team)].shape[0]

def match_won(df, team):
    return df[df['WinningTeam'] == team].shape[0]

def no_result(df, team):
    return df[((df['Team1'] == team) | (df['Team2'] == team)) & (df['WinningTeam'].isnull())].shape[0]



def point_table(season):
    df = ipl[ipl['Season'].astype(str) == str(season)]  # filter matches of selected season

    # get all unique teams who played this season
    teams = np.union1d(df['Team1'].unique(), df['Team2'].unique())

    new_dataframe = pd.DataFrame()
    new_dataframe['Team_name'] = teams

    # calculate match stats for each team
    new_dataframe['Match_played'] = new_dataframe['Team_name'].apply(lambda x: matched_played(df, x))
    new_dataframe['Wins'] = new_dataframe['Team_name'].apply(lambda x: match_won(df, x))
    new_dataframe['No_result'] = new_dataframe['Team_name'].apply(lambda x: no_result(df, x))
    new_dataframe['Losses'] = new_dataframe['Match_played'] - new_dataframe['Wins'] - new_dataframe['No_result']

    # 2 points for a win, 1 point for no result
    new_dataframe['Points'] = new_dataframe['Wins'] * 2 + new_dataframe['No_result']

    new_dataframe.sort_values('Points', ascending=False, inplace=True)  # sort by points
    new_dataframe.set_index('Team_name', inplace=True)  # set index as team name

    return new_dataframe


def point_table_extension(val):
    new_df = point_table(val)  # get base point table
    season_val = str(val)

    new_df['SeasonPosition'] = np.nan  # create empty column for ranking

    # Get winner & runner-up from Final match
    final = ipl[(ipl['Season'] == season_val) & (ipl['MatchNumber'] == 'Final')]
    if not final.empty:
        winner = final['WinningTeam'].values[0]
        team1 = final['Team1'].values[0]
        team2 = final['Team2'].values[0]

        # assign winner and runner-up
        if winner == team1:
            new_df.loc[team1, 'SeasonPosition'] = 'Winner'
            new_df.loc[team2, 'SeasonPosition'] = 'Runner Up'
        else:
            new_df.loc[team2, 'SeasonPosition'] = 'Winner'
            new_df.loc[team1, 'SeasonPosition'] = 'Runner Up'

    # Get 3rd place from Qualifier 2 loser
    qualifier = ipl[(ipl['Season'] == season_val) & (ipl['MatchNumber'] == 'Qualifier 2')]
    if not qualifier.empty:
        winner = qualifier['WinningTeam'].values[0]
        team1 = qualifier['Team1'].values[0]
        team2 = qualifier['Team2'].values[0]
        loser = team2 if winner == team1 else team1
        new_df.loc[loser, 'SeasonPosition'] = '3rd Place'

    # Get 4th place from Eliminator loser
    eliminator = ipl[(ipl['Season'] == season_val) & (ipl['MatchNumber'] == 'Eliminator')]
    if not eliminator.empty:
        winner = eliminator['WinningTeam'].values[0]
        team1 = eliminator['Team1'].values[0]
        team2 = eliminator['Team2'].values[0]
        loser = team2 if winner == team1 else team1
        new_df.loc[loser, 'SeasonPosition'] = '4th Place'

    # Assign 5th, 6th, etc. to remaining teams
    start_rank = 5
    nan_indexes = new_df[new_df['SeasonPosition'].isna()].index
    for i, idx in enumerate(nan_indexes, start=start_rank):
        new_df.at[idx, 'SeasonPosition'] = f"{i}th Place"

    return new_df.reset_index().to_dict(orient='records')  # convert to list of dicts 




def Player_Of_match_details():
     # Merge ball-level and match-level data
    merged_df = balls.merge(ipl, how='inner', on='ID')

    # Get Player of the Match per match
    player_of_match_df = merged_df.groupby(['Season', 'ID'])['Player_of_Match'].first().reset_index()

    # Filter rows where the Player of the Match was the batter
    pom_batting = merged_df[merged_df['batter'] == merged_df['Player_of_Match']]

    # Batting runs and balls faced
    batting_runs = pom_batting.groupby(['Season', 'ID'])['batsman_run'].sum().reset_index()
    balls_faced = pom_batting.groupby(['Season', 'ID'])['ballnumber'].count().reset_index()

    # Calculate bowler-run (ignore legbyes and byes)
    merged_df['bowler_run'] = merged_df['extra_type'].apply(lambda x: 0 if x in ('legbyes', 'byes') else 1)

    # Identify wickets credited to bowler
    merged_df['is_bowler_wicket'] = merged_df['kind'].apply(
        lambda x: 1 if x in ('caught', 'caught and bowled', 'bowled', 'stumped', 'lbw', 'hit wicket') else 0)

    # Filter rows where Player of the Match was the bowler
    pom_bowling = merged_df[merged_df['bowler'] == merged_df['Player_of_Match']]

    # Wickets taken
    bowling_wickets = pom_bowling.groupby(['Season', 'ID'])['is_bowler_wicket'].sum().reset_index()

    # Runs conceded by bowler
    bowling_runs = pom_bowling[pom_bowling['bowler_run'] == 1]
    runs_conceded = bowling_runs.groupby(['Season', 'ID'])['total_run'].sum().reset_index()

    # Merge all data
    final_df = player_of_match_df \
        .merge(batting_runs, how='outer', on=['Season', 'ID']) \
        .merge(balls_faced, how='outer', on=['Season', 'ID']) \
        .merge(bowling_wickets, how='outer', on=['Season', 'ID']) \
        .merge(runs_conceded, how='outer', on=['Season', 'ID'])

    # Create Batting and Bowling Figure strings (e.g., 45/30 or 3/25)
    final_df["Batting_Figure"] = final_df['batsman_run'].astype('Int32').astype(str) + "/" + final_df['ballnumber'].astype('Int32').astype(str)
    final_df["Bowling_Figure"] = final_df['is_bowler_wicket'].astype('Int32').astype(str) + "/" + final_df['total_run'].astype('Int32').astype(str)

    # Final Display
    final=final_df[['Season','ID', 'Player_of_Match', 'Batting_Figure', 'Bowling_Figure']]
    
    return final.to_dict(orient='records')  # clean list of dicts






def get_batter_pair(x):
    return "-".join(list(np.sort(x.values)))  # always sort names alphabetically

def batting_pair():
    # Create new column with batter pairs (e.g. "Dhoni-Kohli"), row-wise
    deliveries['batter_pair'] = deliveries[['batter', 'non-striker']].apply(get_batter_pair, axis=1)

    # Group by each pair and compute total wickets, runs, balls
    newdf = deliveries.groupby('batter_pair').agg({
        "isWicketDelivery": "sum",
        "batsman_run": "sum",
        "ballnumber": "sum",
    })

    # Strike Rate calculation
    newdf['Strike_rate'] = (newdf['batsman_run'] / newdf['ballnumber']) * 100

    # Batting average: If no wickets, use total runs as average
    newdf['Average'] = np.where(
        newdf['isWicketDelivery'] == 0,
        newdf['batsman_run'],
        newdf['batsman_run'] / newdf['isWicketDelivery']
    )
    
    newdf['Average'] = newdf['Average'].round(2)

    # Reset index to treat batter_pair as normal column
    newdf.reset_index(inplace=True)

    # Split batter_pair into Batsman1 and Batsman2
    newdf['Batsman1'] = newdf['batter_pair'].apply(lambda x: x.split('-')[0])
    newdf['Batsman2'] = newdf['batter_pair'].apply(lambda x: x.split('-')[1])

    # Sort by total runs scored
    newdf.sort_values(by=['batsman_run'], ascending=False, inplace=True)

    # Select top 10 pairs, rename columns
    final = newdf[['Batsman1', 'Batsman2', 'batsman_run', 'Average']].head(10)
    final = final.rename(columns={'batsman_run': 'Total Runs'})

    return final.to_dict(orient='records')  # return dict




   