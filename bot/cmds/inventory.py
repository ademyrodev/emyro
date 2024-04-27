from typing import Optional

import nextcord
from nextcord import SlashOption

import bot.game.players as players
from bot.cmd import Cmd


class InventoryCmd(Cmd):
    name = "inventory"
    desc = "Shows the contents of one's inventory."

    async def run(
        self,
        interaction: nextcord.Interaction,
        member: Optional[nextcord.Member] = SlashOption(required=False),
    ):
        user = member or interaction.user
        player = players.find(user.id)
        inventory = player.inventory

        title = f":pouch: {user.name}'s inventory"

        desc = ""
        if inventory.is_empty():
            desc = ":sparkles: **It's empty in here!**"
        else:
            items_format = [f"{i.name} x{i.amount}" for i in inventory.items]

            desc = "".join(items_format)

        embed = nextcord.Embed(title=title, description=desc, color=0x3498DB)
        await interaction.response.send_message(embed=embed)
