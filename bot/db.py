import sqlite3 as sqlite

from bot.logger import Logger

INIT_STMTS = [
    """
    CREATE TABLE IF NOT EXISTS biome_days (
        player_id INT,
        biome_id INT,
        days INT,
        nights INT,

        PRIMARY KEY (player_id, biome_id),
        FOREIGN KEY (player_id) REFERENCES players(id),
        FOREIGN KEY (biome_id) REFERENCES biomes(id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS biomes (
        id INT PRIMARY KEY,
        display TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS divisions (
        id INT PRIMARY KEY,
        display TEXT,
        level INT 
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS players (
        id INT PRIMARY KEY,
        level INT,
        xp INT,
        req_xp INT,
        hp INT,
        energy INT,
        coins INT,
        shards INT,
        weapon TEXT,
        armor TEXT,
        division INT,
        biome INT,
        total_days INT,
        total_nights INT,

        FOREIGN KEY (division) REFERENCES divisions(id),
        FOREIGN KEY (biome) REFERENCES biomes(id)
    )
    """,
    """
    INSERT OR REPLACE INTO biomes VALUES (0, ':herb: Selva Esmeralda')
    """,
    """
    INSERT OR REPLACE INTO biomes VALUES (1, ':desert: Ventana De Llanto')
    """,
    """
    INSERT OR REPLACE INTO biomes VALUES (2, ':mountain_snow: Sérac Glacé')
    """,
    """
    INSERT OR REPLACE INTO biomes VALUES (3, ':evergreen_tree: Dunkelwald')
    """,
    """
    INSERT OR REPLACE INTO divisions VALUES (0, 'Rookie', 1)
    """,
    """
    INSERT OR REPLACE INTO divisions VALUES (1, 'Novice', 30)
    """,
    """
    INSERT OR REPLACE INTO divisions VALUES (2, 'Adept', 50)
    """,
    """
    INSERT OR REPLACE INTO divisions VALUES (3, 'Elite', 100)
    """,
    """
    INSERT OR REPLACE INTO divisions VALUES (4, 'Master', 500)
    """,
    """
    INSERT OR REPLACE INTO divisions VALUES (5, '**Champion**', 750)
    """,
    """
    INSERT OR REPLACE INTO divisions VALUES (6, '**Legend**', 1000)
    """,
    """
    INSERT OR REPLACE INTO divisions VALUES (7, '**Grandmaster**', 2000)
    """,
    """
    INSERT OR REPLACE INTO divisions VALUES (8, '**Sage**', 5000)
    """,
    """
    INSERT OR REPLACE INTO divisions VALUES (9, '**God**', 10000)
    """,
]


class Db:
    conn = sqlite.connect("data.db")

    @staticmethod
    def init():
        cur = Db.conn.cursor()

        for i, s in enumerate(INIT_STMTS):
            cur.execute(s)

        Db.conn.commit()

    @staticmethod
    def raw_exec(stmt: str, *args):
        cur = Db.conn.cursor()

        cur.execute(stmt, args)

        return cur

    @staticmethod
    def commit(stmt: str, *args):
        cur = Db.raw_exec(stmt, *args)

        Db.conn.commit()

    @staticmethod
    def fetch(stmt: str, *args):
        cur = Db.raw_exec(stmt, *args)

        vals = cur.fetchall()

        return vals

    @staticmethod
    def dump(table: str):
        print(Db.fetch(f"SELECT * FROM {table}"))

    @staticmethod
    def close():
        Db.conn.close()
