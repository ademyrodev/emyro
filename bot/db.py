import sqlite3 as sqlite

from bot.game.player import Player
from bot.game.biomes import DayNightCounter
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
        division INT,
        biome INT,

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

    def fetch_biome_ids():
        return Db.fetch("SELECT id FROM biomes")

    @staticmethod
    def fetch_player(player_id: int):
        player_data = Db.fetch(
            "SELECT * FROM players WHERE id = ?", player_id
        ) or Db.register(player_id)

        player_data = player_data[0]

        biome_days = []
        for b in self.fetch_biome_ids():
            days, nights = Db.fetch(
                """
                SELECT days, nights FROM biome_days 
                WHERE player_id = ?, biome_id = ?
                """,
                player_id,
                b
            )

            biome_days.append(
                DayNightCounter(days, nights)
            )

        player_data.append(biome_days)
        
        return player_data
        
    @staticmethod
    def update(player: Player):
        Db.commit(
            """
            UPDATE players SET 
                level = ?,
                xp = ?, 
                req_xp = ?, 
                hp = ?, 
                energy = ?, 
                coins = ?, 
                division = ?,
                biome = ?
            WHERE id = ?
            """,
            player.level,
            player.xp,
            player.req_xp,
            player.hp,
            player.energy,
            player.coins,
            player.division,
            player.biome,
            player.id,
        )

        for b in self.fetch_biome_ids():
            Db.commit(
                """
                UPDATE biome_days SET
                    days = ?,
                    nights = ?
                WHERE player_id = ?, biome_id = ?
                """,
                player.biomes[b].days,
                player.biomes[b].nights,
                player.id,
                b
            )

        Logger.info("Updated player with ID", player.id, "to the database.")

    @staticmethod
    def register(player_id: int):
        player = Player.default(player_id)

        Db.commit(
            "INSERT INTO players VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            player_id,
            player.level,
            player.xp,
            player.req_xp,
            player.hp,
            player.energy,
            player.coins,
            player.division,
            player.biome,
        )

        for b in self.fetch_biome_ids():
            Db.commit(
                "INSERT INTO biome_days VALUES (?, ?, ?, ?)",
                player_id,
                b,
                0,
                0
            )

        Logger.info("Added new player", player_id, "to the database.")

        return Db.fetch("SELECT * FROM players WHERE id = ?", player_id)

    @staticmethod
    def init():
        cur = conn.cursor()

        for i, s in enumerate(INIT_STMTS):
            cur.execute(s)

        conn.commit()

    @staticmethod
    def raw_exec(stmt: str, *args):
        cur = conn.cursor()

        cur.execute(stmt, args)

        return cur

    @staticmethod
    def commit(stmt: str, *args):
        cur = Db.raw_exec(stmt, *args)

        conn.commit()

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
        conn.close()
