import discord
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

    bot = discord.ext.commands.Bot(command_prefix='$', intents=intents)

    # Setup cogs here!
    asyncio.run(setup(bot, Autorole))
    
    bot.run(token)