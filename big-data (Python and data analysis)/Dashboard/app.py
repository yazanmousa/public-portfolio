import json

from flask import Flask, render_template, request

from database import DB

app = Flask(__name__)
db = DB()

menuItems = [
    ['Home', '/'],
    ['Spelers vergelijken', '/compare_players'],
    ['Teams vergelijken', '/compare_team'],
    ['Ontwikkeling', '/history'],
    ['Speler Statistieken', '/players_stats'],
]

"""''''''''''''''''''''''
''' START HOME ROUTES '''
''''''''''''''''''''''"""


@app.route("/")
def index():
    return render_template('home.html', menuItems=menuItems, currentUrl=request.url)


"""''''''''''''''''''''
''' END HOME ROUTES '''
''''''''''''''''''''"""


"""'''''''''''''''''''''''''''''''''
''' START COMPARE PLAYERS ROUTES '''
'''''''''''''''''''''''''''''''''"""


@app.route("/compare_players")
def comparePlayersPage():
    return render_template('compare_players.html', menuItems=menuItems, currentUrl=request.url)


@app.route("/compare_players/<playing_type>/<player_position>/<player_ids>")
def comparePlayersData(playing_type, player_position, player_ids):
    return db.comparePlayers(playing_type, player_position, player_ids).to_json()

@app.route("/compare_players/<type>/<player_ids>")
def getPlayersData(type, player_ids):
    

    csvData = pd.read_csv('2021_' + type + '.csv')
    player_ids = player_ids.split(',')

    players = []
    for player in player_ids:
        players.append(csvData.iloc[int(player)])
        
    names = []
    labels = []
    values = []
    for player in players:
        playerLabels = []
        playerValues = []

        player = player
        for attr, value in player.to_dict().items():
            if attr not in ["index","player","team"]:
                playerLabels.append(attr)
                playerValues.append(value)


        names.append(player['player'])
        labels.append(playerLabels)
        values.append(playerValues)
    return json.dumps([names, labels, values])

"""''''''''''''''''''''''''''''''
''' END COMPARE PLAYER ROUTES '''
''''''''''''''''''''''''''''''"""


"""''''''''''''''''''''''''''''''
''' START COMPARE TEAM ROUTES '''
''''''''''''''''''''''''''''''"""


@app.route("/compare_team")
def compareTeamPage():
    return render_template('compare_team.html', menuItems=menuItems, currentUrl=request.url)


@app.route("/compare_team/<playing_type>/<team>/<player_position>")
def compareTeamData(playing_type, team, player_position):
    return db.teamStats(playing_type, team, player_position).to_json()


@app.route("/compare_team_per_player/<playing_type>/<team>/<player_positions>")
def compare_team_per_player(playing_type, team, player_positions):
    players = db.getPlayersByTeam(playing_type, team)
    player_ids = players['id'].map(str)
    player_ids = player_ids.str.cat(sep=',')

    return db.playerStats(playing_type, player_positions, player_ids).to_json()


"""''''''''''''''''''''''''''''
''' END COMPARE TEAM ROUTES '''
''''''''''''''''''''''''''''"""


"""''''''''''''''''''''''''
''' START Players stats '''
''''''''''''''''''''''''"""


@app.route('/players_stats')
def playersStatsPage():
    return render_template('players_stats.html', menuItems=menuItems, currentUrl=request.url)


@app.route("/players_stats/<playing_type>/<player_positions>/<player_ids>")
def playersStatsData(playing_type, player_positions, player_ids):
    return db.playerStats(playing_type, player_positions, player_ids).to_json()


"""''''''''''''''''''''''
''' END Players stats '''
''''''''''''''''''''''"""


"""''''''''''''''''''''''''''''''
''' START HISTORY DATA ROUTES '''
''''''''''''''''''''''''''''''"""


@app.route('/history')
def historyPage():
    return render_template('history.html', menuItems=menuItems, currentUrl=request.url)


@app.route("/history/<playing_type>/<player_position>/<player_ids>")
def history(playing_type, player_position, player_ids):
    results = db.history(playing_type, player_position, player_ids)

    return json.dumps(results)


"""''''''''''''''''''''''''''''
''' END HISTORY DATA ROUTES '''
''''''''''''''''''''''''''''"""


"""'''''''''''''''''''''
''' START API ROUTES '''
'''''''''''''''''''''"""


@app.route("/get_teams")
def get_teams():
    return db.getTeams().to_json()


@app.route("/get_positions/<type>")
def get_positions(type):
    return db.getPlayerPositionsByPlayingType(type).to_json()


@app.route("/get_players/<playing_type>/<player_position>")
def get_players(playing_type, player_position):
    return db.getPlayersByPosition(playing_type, player_position).to_json()


@app.route("/get_players_by_positions/<playing_type>/<player_positions>")
def get_players_by_positions(playing_type, player_positions):
    return db.getPlayersByPositions(playing_type, player_positions).to_json()


@app.route("/get_players_by_team/<playing_type>/<team>")
def get_players_by_team(playing_type, team):
    return db.getPlayersByTeam(playing_type, team).to_json()


"""'''''''''''''''''''
''' END API ROUTES '''
'''''''''''''''''''"""

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
