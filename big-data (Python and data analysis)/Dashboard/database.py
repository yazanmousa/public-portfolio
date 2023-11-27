from pandas.core.frame import DataFrame
from sqlalchemy import create_engine
import pandas as pd


class DB:
    def __init__(self) -> None:
        self.engine = create_engine(
            'mysql://baseball:baseball@db/baseball'
        )

    def getPlayerPositionsByPlayingType(self, playingType) -> pd.DataFrame:
        results = pd.read_sql_query('SHOW COLUMNS FROM `{table}`'.format(
            table=playingType), con=self.engine)
        results = results[3:]

        return results['Field']

    def getPlayersByPosition(self, playing_type, player_position) -> pd.DataFrame:
        results = pd.read_sql_query("""
            SELECT 
                `player`.`id`, 
                `player`.`fullname` 
            FROM `{table}`
            INNER JOIN `player` ON `{table}`.`player_id` = `player`.`id`
            WHERE `{row}` > 0
            GROUP BY `player`.`id`
            ORDER BY `player`.`fullname` ASC
        """.format(table=playing_type, row=player_position), con=self.engine)

        return results

    def getTeams(self) -> pd.DataFrame:
        results = pd.read_sql_query("""
            SELECT
                DISTINCT(`team`) AS `team`
            FROM `match`
            ORDER BY `team` ASC
        """.format(), con=self.engine)

        return results

    def getPlayersByPositions(self, playing_type, player_positions) -> pd.DataFrame:
        results = pd.read_sql_query("""
            SELECT 
                `player`.`id`, 
                `player`.`fullname` 
            FROM `{table}`
            INNER JOIN `player` ON `{table}`.`player_id` = `player`.`id`
            GROUP BY `player`.`id`
            ORDER BY `player`.`fullname` ASC
        """.format(table=playing_type), con=self.engine)

        return results

    def getPlayersByTeam(self, playing_type, team) -> pd.DataFrame:
        results = pd.read_sql_query("""
            SELECT 
                `player`.`id`, 
                `player`.`fullname` 
            FROM `match`

            INNER JOIN `{table}` ON `{table}`.match_id = `match`.`id`
            INNER JOIN `player` ON `player`.id = `{table}`.`player_id`

            WHERE `match`.`team` = '{team}'

            GROUP BY `player`.`id`
            ORDER BY `player`.`fullname` ASC
        """.format(table=playing_type, team=team), con=self.engine)

        return results

    def comparePlayers(self, playing_type, player_position, player_ids) -> pd.DataFrame:
        results = pd.read_sql_query("""
            SELECT 
                `player`.`fullname`,
                SUM(`{table}`.`{row}`) as score
            FROM `player`
            INNER JOIN `{table}` ON `{table}`.`player_id` = `player`.`id`
            INNER JOIN `match` ON `match`.`id` = `{table}`.`match_id`

            WHERE `player`.`id` IN ({ids})

            GROUP BY `player`.`id`
            ORDER BY `player`.`fullname` ASC
        """.format(table=playing_type, row=player_position, ids=player_ids), con=self.engine)

        return results

    def history(self, playing_type, player_position, player_ids) -> list:
        results = pd.read_sql_query("""
            SELECT 
                `player`.`id`,
                `player`.`fullname`,
                SUM(`{table}`.`{row}`) AS `score`,
                DATE_FORMAT(`date`, '%%Y') AS `year`
            FROM `player`

            INNER JOIN `{table}` ON `{table}`.`player_id` = `player`.`id`
            INNER JOIN `match` ON `match`.`id` = `{table}`.`match_id`

            WHERE `player`.`id` IN ({ids})
            AND DATE_FORMAT(`date`, '%%Y') >= DATE_FORMAT(DATE(NOW()-INTERVAL 10 YEAR), '%%Y')

            GROUP BY `player`.`id`, DATE_FORMAT(`date`, '%%Y')

            ORDER BY `player`.`fullname` ASC, `year` ASC
        """.format(table=playing_type, row=player_position, ids=player_ids), con=self.engine)

        results = results.to_numpy()

        players = {}

        for row in results:
            players[row[1]] = {'years': [], 'scores': []}

        for row in results:
            players[row[1]]['scores'].append(row[2])
            players[row[1]]['years'].append(row[3])

        return players

    def playerStats(self, playing_type, player_positions, player_ids) -> pd.DataFrame:
        player_positions = player_positions.split(',')
        select = ''
        for pos in player_positions:
            select = select + 'SUM(`{table}`.`{pos}`) AS `{pos}`,'.format(table=playing_type, pos=pos)

        select = select[:-1]

        results = pd.read_sql_query("""
            SELECT 
                `player`.`id`,
                `player`.`fullname`,
                {select}
            FROM `player`

            INNER JOIN `{table}` ON `{table}`.`player_id` = `player`.`id`

            WHERE `player`.`id` IN ({ids})

            GROUP BY `player`.`id`
            ORDER BY `player`.`fullname` ASC
        """.format(table=playing_type, ids=player_ids, select=select), con=self.engine)

        return results

    def teamStats(self, playing_type, team, player_position) -> pd.DataFrame:
        results = pd.read_sql_query("""
            SELECT
                `player`.`fullname`,
                SUM(`{table}`.`{row}`) AS score
            FROM `player`

            INNER JOIN `batting` ON `{table}`.`player_id` = `player`.`id`
            INNER JOIN `match` ON `match`.id = `batting`.`match_id`

            WHERE `match`.`team` = '{team}'

            GROUP BY `player`.`id`
            ORDER BY `player`.`fullname` ASC
        """.format(table=playing_type, team=team, row=player_position), con=self.engine)

        return results
