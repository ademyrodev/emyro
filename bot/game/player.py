import bot.game.biomes as biomes
from bot.db import Db
from bot.game.biomes import DayNightCounter
from bot.game.equipment import Equipment
from bot.game.inventory import Inventory
from bot.logger import Logger


class Player:
    def __init__(
        self,
        id: int,
        level: int,
        xp: int,
        req_xp: int,
        hp: int,
        energy: int,
        coins: int,
        shards: int,
        weapon: Equipment,
        armor: Equipment,
        division: int,
        biome: int,
        total_days: DayNightCounter,
        biomes: list[DayNightCounter],
        inventory: Inventory,
    ):

        self.id = id
        self.level = level
        self.xp = xp
        self.req_xp = req_xp
        self.hp = hp
        self.energy = energy
        self.coins = coins
        self.shards = shards
        self.weapon = weapon
        self.armor = armor
        self.division = division
        self.biome = biome
        self.total_days = total_days
        self.biomes = biomes
        self.inventory = inventory

    @staticmethod
    def default(id):
        biomes = [DayNightCounter.default()] * 4

        return Player(
            id,
            1,
            0,
            25,
            100,
            50,
            0,
            0,
            Equipment.none(),
            Equipment.none(),
            0,
            0,
            DayNightCounter.default(),
            biomes,
            Inventory.empty(),
        )

    @staticmethod
    def from_raw(data):
        total_days = data[-4]
        total_nights = data[-3]

        data[-4] = DayNightCounter(total_days, total_nights)
        del data[-3]

        return Player(*data)

    @staticmethod
    def fetch_from_db(player_id: int):
        player_data = Db.fetch(
            "SELECT * FROM players WHERE id = ?", player_id
        ) or Player.register(player_id)

        player_data = list(player_data[0])

        weapon_json = player_data[8]
        armor_json = player_data[9]

        weapon = Equipment.from_json(weapon_json)
        armor = Equipment.from_json(armor_json)

        player_data[8] = weapon
        player_data[9] = armor

        biome_days = []
        for b in biomes.ids():
            days, nights = Db.fetch(
                """
                SELECT days, nights FROM biome_days 
                WHERE player_id = ? AND biome_id = ?
                """,
                player_id,
                b,
            )[0]

            counter = DayNightCounter(days, nights)
            biome_days.append(counter)

        player_data.append(biome_days)

        inventory_json = Db.fetch(
            """
            SELECT content FROM inventories
            WHERE player_id = ?
            """,
            player_id,
        )[0][0]

        inventory = Inventory.from_json(inventory_json)

        player_data.append(inventory)

        return Player.from_raw(player_data)

    @staticmethod
    def register(player_id: int):
        player = Player.default(player_id)

        Db.commit(
            "INSERT INTO players VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            player_id,
            player.level,
            player.xp,
            player.req_xp,
            player.hp,
            player.energy,
            player.coins,
            player.shards,
            player.weapon.json(),
            player.armor.json(),
            player.division,
            player.biome,
            player.total_days.days,
            player.total_days.nights,
        )

        for b in biomes.ids():
            Db.commit("INSERT INTO biome_days VALUES (?, ?, ?, ?)", player_id, b, 0, 0)

        Db.commit(
            "INSERT INTO inventories VALUES (?, ?)", player_id, player.inventory.json()
        )

        Logger.info("Added new player", player_id, "to the database.")

        return [Db.fetch("SELECT * FROM players WHERE id = ?", player_id)]

    def update(self):
        Db.commit(
            """
            UPDATE players SET 
                level = ?,
                xp = ?, 
                req_xp = ?, 
                hp = ?, 
                energy = ?, 
                coins = ?, 
                shards = ?,
                weapon = ?,
                armor = ?,
                division = ?,
                biome = ?,
                total_days = ?,
                total_nights = ?
            WHERE id = ?
            """,
            self.level,
            self.xp,
            self.req_xp,
            self.hp,
            self.energy,
            self.coins,
            self.shards,
            self.weapon.json(),
            self.armor.json(),
            self.division,
            self.biome,
            self.total_days.days,
            self.total_days.nights,
            self.id,
        )

        Db.commit(
            """
            UPDATE inventories SET
                content = ?
            WHERE player_id = ?
            """,
            self.inventory.json(),
            self.id,
        )

        for b in biomes.ids():
            Db.commit(
                """
                UPDATE biome_days SET
                    days = ?,
                    nights = ?
                WHERE player_id = ? AND biome_id = ?
                """,
                self.biomes[b].days,
                self.biomes[b].nights,
                self.id,
                b,
            )

        Logger.info("Updated player with ID", self.id, "to the database.")
