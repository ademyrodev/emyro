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

        title = f":scroll: | {user.name}"
        embed = nextcord.Embed(title=title, color=0xFF0000)

        embed.add_field(
            name=":fleur_de_lis: Division", value=self.division_desc(player)
        )

        embed.add_field(name=":star: Level", value=str(player.level))

        embed.add_field(
            name=":sparkles: XP", value=ui.progress_bar(player.xp, player.req_xp)
        )

        # not actually a progress bar, we're tricking players here
        hp_bar = ui.progress_bar(player.hp, player.hp, show_percent=False)
        embed.add_field(name=":heart: HP", value=hp_bar)

        # same story here
        energy_bar = ui.progress_bar(player.energy, player.energy, show_percent=False)
        embed.add_field(name=":zap: Energy", value=energy_bar)

        embed.add_field(name=":coin: Coins", value=player.coins)

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
        """
