import nextcord

import bot.db as db
import bot.game.players as players
from bot.cmd import Cmd


class BiomesCmd(Cmd):
    name = "biomes"
    desc = "Lists all available biomes."

    async def run(self, interaction: nextcord.Interaction):
        biomes = db.fetch("SELECT * FROM biomes")

        embed = nextcord.Embed(title="🌲 | Biomes", color=0x50C878)

        player = players.find(interaction.user.id)

        for b in biomes:
            biome_id = b[0]
            biome_name = b[1]
            desc = "**You're currently here!**" if player.biome == biome_id else ""

            embed.add_field(name=biome_name, value=desc)

        await interaction.response.send_message(embed=embed)
