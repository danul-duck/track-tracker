import sqlite3 
import os 
import yaml

def setup():
    conn =  sqlite3.connect("main.db")
    cur = conn.cursor()
    dirname = os.path.dirname(__file__)

    with open(f'{dirname}/../config.yaml','r') as f :
        config = yaml.safe_load(f)
    
    _create_table = """
        CREATE TABLE IF NOT EXISTS {} (
            track TEXT, 
            player TEXT,
            active INTEGER,
            dttm TEXT, 
            record REAL,
        PRIMARY KEY (track, player, dttm)
        )
        """
    for season in config['tracks'].keys() :
        print(_create_table.format(season))
        cur.execute(_create_table.format(season))
        conn.commit()
    
    conn.close()


if __name__ == '__main__':
    setup()
