import discord
from discord.ext import commands
from discord import app_commands

import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

token = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.guild_scheduled_events = True
intents.guilds = True

activity = discord.Activity(type=discord.ActivityType.watching, name="Maintenance")

bot = commands.Bot(command_prefix=';', intents=intents, activity=activity)

format = [
    'nama',
    'nama panggilan',
    'angkatan',
    'hobi',
    'minat'
]

allowed_role = ['Bapak Informatikans', 'Staf']
reminder_intervals = [1, 3] # Days before event to send reminder

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Error syncing commands: {e}")

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
            
        print(message.content.lower())
        role = discord.utils.get(message.guild.roles, name="Informatikans")
        await message.add_reaction('👋')
        await message.channel.send(f'{message.author.mention} Salam kenal, {nickname.strip().title()}! Selamat bergabung di Informatikans!')
        await message.author.add_roles(role)

@bot.tree.command(name="ping", description="Check bot latency")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f':ping_pong: Pong! `{round(bot.latency * 1000)}`ms')

TEMPLATE_KERNEL = """
📢✨ 𝐃-{days_left} 𝐊𝐄𝐑𝐍𝐄𝐋 𝐒𝐄𝐒𝐒𝐈𝐎𝐍  ✨📢

Halo, Informatikans!! @everyone

KERNEL SESSION is BACK!! 🤩🤯
KERNEL Session kali ini mengusung tema {theme}

{description}

SAVE THE DATE! ‼️
🗓️: {date_event_in_ID}
⏰: {time} WIB-selesai
📍: https://bit.ly/Informatikans (Server Discord Informatikans)
🔗: https://discord.gg/qGM3gYt6?event=1305395013529632798

:head_shaking_horizontally: Don't miss out! :head_shaking_horizontally:

Best Regards,
Departemen Akademik
{dept_name}
HMIF UPNVJ {year}

#{dept_name_nospaces}
#MenuntunIlmu
"""

@bot.tree.command(
    name="schedule_event", description="Schedule an event with a date and description"
)
@app_commands.describe(
    date="Date in the format DD-MM-YYYY",
    time="Time in the format HH:MM",
    theme="Event theme",
    description="Event description",
    dept_name="Department name",
)
async def schedule_event(
    interaction: discord.Interaction,
    date: str,
    time: str,
    theme: str,
    description: str,
    dept_name: str,
):
    member = await interaction.guild.fetch_member(interaction.user.id)

    if any(role in allowed_role for role in [role.name for role in member.roles]):
        try:
            event_time = datetime.strptime(date, "%d-%m-%Y")

            date_event_in_ID = event_time.strftime("%A, %d %B %Y")
            date_now = datetime.now()

            date_day_difference = (event_time - date_now).days
            year = datetime.now().year

            guild = bot.get_guild(interaction.guild.id)

            if not guild:
                await interaction.response.send_message("This command must be invoked in a guild.", ephemeral=True)
                return
            
            channel = discord.utils.get(guild.text_channels, name="bot")
            if not channel:
                await interaction.response.send_message("Channel 'bot' not found.", ephemeral=True)
                return
            
            discord_event = await guild.create_scheduled_event(
                name=f"KERNEL Session: {theme}",
                start_time=event_time,
                end_time=event_time,
                description=TEMPLATE_KERNEL.format(
                    days_left=date_day_difference,
                    theme=theme,
                    description=description,
                    date_event_in_ID=date_event_in_ID,
                    time=time,
                    dept_name=dept_name,
                    dept_name_nospaces=dept_name.replace(" ", ""),
                    year=year,
                ),
                location="https://discord.gg/qGM3gYt6?event=1305395013529632798",
                privacy_level=discord.PrivacyLevel.guild_only,
            )

            await interaction.response.send_message(f"Event scheduled: {discord_event.url}")

            # if date_day_difference == 0:
            #     await interaction.response.send_message(
            #         TEMPLATE_KERNEL.format(
            #             day="DAY",
            #             theme=theme,
            #             description=description,
            #             date_event_in_ID=date_event_in_ID,
            #             time=time,
            #             dept_name=dept_name,
            #             dept_name_nospaces=dept_name.replace(" ", ""),
            #             year=year,
            #         )
            #     )
            # else:
            #     await interaction.response.send_message(
            #         TEMPLATE_KERNEL.format(
            #             day=date_day_difference,
            #             theme=theme,
            #             description=description,
            #             date_event_in_ID=date_event_in_ID,
            #             time=time,
            #             dept_name=dept_name,
            #             dept_name_nospaces=dept_name.replace(" ", ""),
            #             year=year,
            #         )
            #     )
        except ValueError:
            await interaction.response.send_message(
                "Invalid date format! Please use DD-MM-YYYY.", ephemeral=True
            )
        except discord.Forbidden:
            await interaction.response.send_message(
                "I do not have permission to create a scheduled event."
            )
    else:
        await interaction.response.send_message(
            "You do not have permission to use this command."
        )

bot.run(token)