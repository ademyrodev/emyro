import nextcord
import bot.game.players as players
import bot.game.division as division
import bot.ui as ui

from bot.cmd import Cmd

class StatsCmd(Cmd):
    name = "stats"
    desc = "Shows one's stats."

    async def run(self, interaction: nextcord.Interaction):
        username = interaction.user.name
        player = players.find(interaction.user.id)
        
        title = f"📜 | {username}'s profile"
        embed = nextcord.Embed(title=title, color=0xff0000)

        embed.add_field(
            name="⚜️ Division", value=division.display(player.division)
        )
        
        embed.add_field(
            name="⭐ Level", value=str(player.level)
        )

        embed.add_field(
            name="✨ XP", value=ui.progress_bar(player.xp, player.req_xp)
        )

        # not actually a progress bar, we're tricking players here
        hp_bar = ui.progress_bar(player.hp, player.hp, show_percent=False)
        embed.add_field(
            name="❤️ HP", value=hp_bar
        )

        # same story here
        energy_bar = ui.progress_bar(player.energy, player.energy, show_percent=False)
        embed.add_field(
            name="⚡ Energy", value=energy_bar
        )

        embed.add_field(
            name="🪙 Coins", value=player.coins
        )

        await interaction.response.send_message(embed=embed)
