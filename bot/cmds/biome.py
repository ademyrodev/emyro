from typing import Optional

import nextcord
from nextcord import SlashOption

import bot.db as db
import bot.game.biomes as biomes
import bot.game.players as players
from bot.cmd import Cmd


class BiomeCmd(Cmd):
    name = "biome"
    desc = "Shows one's current biome."

    async def run(
        self,
        interaction: nextcord.Interaction,
        member: Optional[nextcord.Member] = SlashOption(required=False),
    ):
        player = None

        if not member:
            player = players.find(interaction.user.id)
        else:
            player = players.find(member.id)

        biome_name = biomes.display(player.biome)

        if not member:
            await interaction.response.send_message(
                f"**You're currently in __{biome_name}__.**\n"
                "You can change biomes using the `/biome move` command.  (currently unimplemented.)"
            )
        else:
            await interaction.response.send_message(
                f"**{member.name} is currently in __{biome_name}__.**"
            )
