import nextcord

from datetime import datetime

from bot.game.world import World
from bot.cmd import Cmd

class TimeCmd(Cmd):
    name = "time"
    desc = "Tells the user whether it is currently day time or night time"

    async def run(self, interaction: nextcord.Interaction):
        display = ":sunny: Day time" if World.daytime else ":crescent_moon: Night time"
        opposite = "night time" if World.daytime else "day time"

        now = datetime.now()

        elapsed_time = now.minute - World.last_daytime_flip

        # if a rollover to the next hour happened
        if elapsed_time < World.day_length - 60:
            elapsed_time += 60

        time_left_msg = ""
        if elapsed_time == 9:
            time_left_msg = f"{60 - now.second} seconds left"
        else:
            time_left_msg = f"{10 - elapsed_time} minutes left"

        await interaction.response.send_message(
            f"It is currently **{display}**!\n"
            f"**{time_left_msg}** until __{opposite}__!"
        )
