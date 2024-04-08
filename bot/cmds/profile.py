from typing import Optional

import nextcord
from nextcord import SlashOption

import bot.game.divisions as divisions
import bot.game.players as players
import bot.ui as ui
from bot.cmd import Cmd
from bot.game.player import Player


class ProfileCmd(Cmd):
    name = "profile"
    desc = "Shows one's profile."

    async def run(
        self,
        interaction: nextcord.Interaction,
        member: Optional[nextcord.Member] = SlashOption(required=False),
    ):
        user = member or interaction.user
        player = players.find(user.id)

        title = f":scroll: {user.name}"
        embed = nextcord.Embed(title=title, color=0xFF0000)

        embed.add_field(
            name=":bar_chart: Stats", 
            value=f"""
            :heart: HP: {ui.progress_bar(player.hp, player.hp, show_percent=False)}
            :zap: Energy: {ui.progress_bar(player.energy, player.energy, show_percent=False)} 
            :dagger: Weapon: {player.weapon.name} 
            :shield: Armor: {player.armor.name}
            """
        )

        embed.add_field(
            name=":rocket: Leveling", 
            value=f"""
            :star: Level: {player.level}
            :sparkles: XP: {ui.progress_bar(player.xp, player.req_xp)}
            {self.division_desc(player)}
            """
        )


        embed.add_field(
            name=":moneybag: Purse",
            value=f"""
            :coin: Coins: {player.coins}
            :gem: Shards: {player.shards}
            """
        )

        await interaction.response.send_message(embed=embed)

    def division_desc(self, player: Player):
        next_division = divisions.next(player.division)

        if not next_division:
            return divisions.display(player.division)

        next_division_name = next_division[1]
        next_division_level = next_division[2]

        required = next_division_level - player.level

        return f"""
        {divisions.display(player.division)}
        {next_division_name} **unlocked in {required} more levels!**  
        """.strip()
