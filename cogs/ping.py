import discord
from discord.ext import commands
from discord import app_commands

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('INFO: Ping is ON.')

    @commands.command(
        name="ping",
        description="Pong!",
    )
    async def ping(self, ctx):
        await ctx.send(f"Pong! :ping_pong: `{round(self.bot.latency * 1000)}`ms")

    @app_commands.command(name="ping", description="Check the bot's latency")
    async def ping_slash(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Pong! :ping_pong: `{round(self.bot.latency * 1000)}`ms")

async def setup(bot):
    await bot.add_cog(Ping(bot))