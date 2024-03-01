import os

from dotenv import load_dotenv

load_dotenv()


class Emyro:
    token: str = os.getenv("TOKEN")
    guilds: list[str] = [os.getenv("GUILD")]
