from typing import Optional

import nextcord
from nextcord import SlashOption

import bot.game.players as players
from bot.cmd import Cmd

class SpellbookCmd(Cmd):
    name = "spellbook"
    desc = "Shows one's current set of spells."

    async def run(
        self,
        interaction: nextcord.Interaction,
        member: Optional[nextcord.Member] = SlashOption(required=False)
    ):
        user = member or interaction.user
        player = players.find(user.id)
        spellbook = player.spellbook

        embed = nextcord.Embed(title=f":bookmark: {user.name}'s spellbook", color=0xFFFFFF)
        
        for s in spellbook:
            embed.add_field(
                name=s.name,
                value=f"{s.nature.__repr__()}\n"
                f"{s.intent.__repr__()}\n"
                f"**{s.intensity.name.capitalize()}**\n"
                f"{s.side_effect or 'No side effect'}\n"
                f"{s.cost} :zap:"
            )

        await interaction.response.send_message(embed=embed)