import discord
from discord.ext import commands

import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

token = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guilds = True
intents.guild_scheduled_events = True

activity = discord.Game(name="with Informatikans | use $")

bot = commands.Bot(command_prefix='$', intents=intents)

initial_extensions = [
    'cogs.autorole',
    'cogs.ping',
    'cogs.event',
]

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print('------')
    sync_slash_commands = await bot.tree.sync()
    print(f"Synced {len(sync_slash_commands)} slash commands")
    await bot.change_presence(activity=activity)

async def main():
    for extension in initial_extensions:
        await bot.load_extension(extension)

    await bot.start(token)

if __name__ == '__main__':
    asyncio.run(main())

    # bot.run(token)