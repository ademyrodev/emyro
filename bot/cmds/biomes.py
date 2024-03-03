import nextcord

import bot.game.biomes as biomes
import bot.game.players as players
from bot.cmd import Cmd


class BiomesCmd(Cmd):
    name = "biomes"
    desc = "Lists all available biomes."

    async def run(self, interaction: nextcord.Interaction):
        embed = nextcord.Embed(title=":evergreen_tree: | Biomes", color=0x50C878)

        player = players.find(interaction.user.id)

        for b in biomes.ids():
            biome_name = biomes.display(b)

            days, nights = player.biomes[b].as_tuple()

            desc = f"{days} days | {nights} nights\n"
            details = "**You're currently here!**" if player.biome == b else ""

            embed.add_field(name=biome_name, value=desc + details)

        await interaction.response.send_message(embed=embed)
