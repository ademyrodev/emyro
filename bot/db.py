import sqlite3 as sqlite

INIT_STMTS = [
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
        division INT,
        biome INT,

        FOREIGN KEY (division) REFERENCES divisions(id),
        FOREIGN KEY (biome) REFERENCES biomes(id)
    )
    """,
    """
    INSERT OR REPLACE INTO biomes VALUES (0, 'Selva Esmeralda')
    """,
    """
    INSERT OR REPLACE INTO biomes VALUES (1, 'Ventada De Llanto')
    """,
    """
    INSERT OR REPLACE INTO biomes VALUES (2, 'Sérac Glacé')
    """,
    """
    INSERT OR REPLACE INTO biomes VALUES (3, 'Dunkelwald')
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

conn = sqlite.connect("data.db")


def init():
    cur = conn.cursor()

    for i, s in enumerate(INIT_STMTS):
        cur.execute(s)

    conn.commit()


def raw_exec(stmt: str, *args):
    cur = conn.cursor()

    cur.execute(stmt, args)

    return cur


def commit(stmt: str, *args):
    cur = raw_exec(stmt, *args)

    conn.commit()


def fetch(stmt: str, *args):
    cur = raw_exec(stmt, *args)

    vals = cur.fetchall()

    return vals


def dump(table):
    print(fetch(f"SELECT * FROM {table}"))


def close():
    conn.close()
