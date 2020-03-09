import pymysql
import parcer
import config
from contextlib import closing
from pymysql.cursors import DictCursor

con = config.connection


def extract(connect):
    with connect:
        cur = connect.cursor()
        cur.execute(f"SELECT * FROM {parcer.db}")
        heroes = cur.fetchall()
        export = []

        for hero in heroes:
            export.append( [f"Heroname: {hero['heroname_as_dotaname']}",f"picks: {hero['picks']}",f"wins: {hero['wins']}",f"winrate: {hero['winrate']}",f"pickrate: {hero['pickrate']}"] )

        return export

def export(connect):
    with connect:
        cur = connect.cursor()
        parced_table = parcer.parce(parcer.get_html(parcer.url))

        for hero_stats in parced_table:
            sql_command = f"INSERT INTO {parcer.db} (heroname_as_dotaname,picks,wins,winrate,pickrate) \
                            VALUES ('{hero_stats['heroname_as_dotaname']}','{hero_stats['picks']}','{hero_stats['wins']}','{hero_stats['winrate']}','{hero_stats['pickrate']}')"
            cur.execute(sql_command)

def update(connect):
    cur = connect.cursor()
    parced_table = parcer.parce(parcer.get_html(parcer.url))

    for hero_stats in parced_table:
        sql_command = f"UPDATE {parcer.db} SET picks = {hero_stats['picks']}, wins = {hero_stats['wins']}, winrate = {hero_stats['winrate']}, pickrate = {hero_stats['pickrate']}\
                        WHERE heroname_as_dotaname = '{hero_stats['heroname_as_dotaname']}'"
        cur.execute(sql_command)
        con.commit()

def main():
    update(con)

if __name__ == "__main__":
    main()