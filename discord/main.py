# Copyright © William Adams 2023, licensed under Mozilla Public License Version 2.0

import disnake
from disnake.ext import commands
import os
from dotenv import load_dotenv

#Define intents for bot (make these more specific later so bot doesn't require unnecessary intents/permissions)
intents = disnake.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True


#Get config for bot
config = getConfig()


if config[1] == True:
    bot = commands.Bot(
    test_guilds=["change_this"],
    command_sync_flags=commands.CommandSyncFlags.all(),
    intents=intents,
    activity = disnake.Activity(type=disnake.ActivityType.watching, name="the news"),
)

@bot.event
async def on_ready():
    print("------")
    print(f"Logged in as {bot.user}")
    print("------")

load_dotenv()
bot.run(os.getenv('DISCORD_TOKEN'))