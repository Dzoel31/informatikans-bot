import discord
from discord.ext import commands
from discord import app_commands

import asyncio
import os
import asyncio

from dotenv import load_dotenv
from cogs.autorole import Autorole

load_dotenv()

async def setup(bot, cog):
    await bot.add_cog(cog(bot))

if __name__ == '__main__':
    token = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.guild_scheduled_events = True
intents.guilds = True

activity = discord.Activity(type=discord.ActivityType.watching, name="Maintenance")

    bot = discord.ext.commands.Bot(command_prefix='$', intents=intents)

    # Setup cogs here!
    asyncio.run(setup(bot, Autorole))
    
    bot.run(token)