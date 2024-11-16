import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

activity = discord.Activity(type=discord.ActivityType.watching, name="Informatikans | use ;")

bot = commands.Bot(command_prefix=';', intents=intents, activity=activity)

client = discord.Client(intents=intents)

format = [
    'nama',
    'nama panggilan',
    'angkatan',
    'hobi',
    'minat'
]

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.channel.id != 1237280039771439226:
        return
    
    if all(item in message.content.lower() for item in format):
        message_content = [msg.split(':') for msg in message.content.split('\n')]
        for index, content in enumerate(message_content):
            if any('panggilan' in cont.lower() for cont in content):
                nickname = message_content[index][1]
                break
            
        print(message.content)
        role = discord.utils.get(message.guild.roles, name="Informatikans")
        await message.add_reaction('👋')
        await message.channel.send(f'{message.author.mention} Salam kenal, {nickname.strip().title()}! Selamat bergabung di Informatikans!')
        await message.author.add_roles(role)

@bot.command(name='ping')
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

bot.run(token)