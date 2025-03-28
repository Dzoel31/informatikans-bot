import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta
from pytz import timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from PIL import Image

import dotenv
import os

dotenv.load_dotenv()

"""
This cog demonstrates how to create a scheduled event using the Discord API.
Unfortunately, we have several issues with the current implementation:
1. The `create_event` cannot load the image from the URL.
2. The description cannot be performed in multiple lines.

To handle these issues, we recommend to edit the event from the Discord Menu.
"""

scheduler = AsyncIOScheduler()


class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.role = None
        self.channel_announce = 1235251540751548526 # ID Channel bot untuk testing

    @commands.Cog.listener()
    async def on_ready(self):
        print("INFO: Event is ready.")
        if not scheduler.running:
            scheduler.start()

    async def send_reminder(self, channel, event, reminder_text, start_time):
        print(
            f"INFO: Attempting to send reminder '{reminder_text}' for event '{event.name}'"
        )
        if reminder_text == "Sekarang":
            await channel.send(
                f">>> [{event.name}]({event.url}) sudah dimulai! <@&{self.role.id}>"  #
            )
        else:
            await channel.send(
                f">>> {reminder_text} menuju event [{event.name}]({event.url}) pada {start_time.strftime('%d-%m-%Y %H:%M')} <@&{self.role.id}>."
            )

    @commands.Cog.listener()
    async def on_scheduled_event_create(self, event):
        print("INFO: Event created:", event.name)
        guild = event.guild
        channel = guild.get_channel(self.channel_announce)

        now = datetime.now(timezone("Asia/Jakarta"))
        start_time = event.start_time.astimezone(timezone("Asia/Jakarta"))
        # end_time = event.end_time.astimezone(timezone("Asia/Jakarta"))

        reminders = [
            ("H-7", start_time - timedelta(days=7)),
            ("H-5", start_time - timedelta(days=5)),
            ("H-3", start_time - timedelta(days=3)),
            ("H-1", start_time - timedelta(days=1)),
            ("12 jam", start_time - timedelta(hours=12)),
            ("6 jam", start_time - timedelta(hours=6)),
            ("3 jam", start_time - timedelta(hours=3)),
            ("1 jam", start_time - timedelta(hours=1)),
            ("30 menit", start_time - timedelta(minutes=30)),
            ("15 menit", start_time - timedelta(minutes=15)),
            ("5 menit", start_time - timedelta(minutes=5)),
            ("Sekarang", start_time),
        ]

        for reminder_text, reminder_time in reminders:
            if reminder_time > now:
                print(f"INFO: Scheduling reminder '{reminder_text}' at {reminder_time}")
                scheduler.add_job(
                    self.send_reminder,
                    "date",
                    run_date=reminder_time,
                    args=[channel, event, reminder_text, start_time],
                )
            else:
                print(
                    f"WARNING: Skipping reminder '{reminder_text}' because it's in the past: {reminder_time}"
                )

        await channel.send(
            f"Event [{event.name}]({event.url}) has been successfully created and scheduled for {start_time.strftime('%d-%m-%Y %H:%M')}."
        )

    @app_commands.command(name="create_event", description="Create a scheduled event")
    @app_commands.describe(
        name="Name of the event",
        desc="Description of the event",
        image="URL of the image",
        channel_id="Location of the event",
        start_time="Start time (DD-MM-YYYY HH:MM)",
        end_time="End time (DD-MM-YYYY HH:MM)",
        role="Role to be pinged (default: everyone)",
    )
    async def create_event(
        self,
        interaction: discord.Interaction,
        name: str,
        desc: str,
        image: str | None,
        role: discord.Role | None,
        channel_id: str,
        start_time: str,
        end_time: str,
    ):
        try:
            # Parsing tanggal dan waktu
            start_time_naive = datetime.strptime(start_time, "%d-%m-%Y %H:%M")
            end_time_naive = datetime.strptime(end_time, "%d-%m-%Y %H:%M")

            # Mengonversi waktu menjadi timezone-aware
            start_time_aware = start_time_naive.astimezone()
            end_time_aware = end_time_naive.astimezone()

            guild = interaction.guild
            if not guild:
                await interaction.response.send_message(
                    "This command can only be used in a server.", ephemeral=True
                )
                return

            # Mendapatkan channel dari ID
            channel = guild.get_channel(int(channel_id))
            if not channel:
                await interaction.response.send_message(
                    "Invalid channel ID.", ephemeral=True
                )
                return

            # Menentukan tipe entity berdasarkan channel
            if isinstance(channel, discord.VoiceChannel):
                entity_type = discord.EntityType.voice
            elif isinstance(channel, discord.StageChannel):
                entity_type = discord.EntityType.stage_instance
            else:
                await interaction.response.send_message(
                    "Channel must be a voice or stage channel.", ephemeral=True
                )
                return
            
            self.role = role if role else guild.default_role

            # Membuat scheduled event dengan `channel` jika entity_type adalah voice atau stage
            event = await guild.create_scheduled_event(
                name=name,
                description=desc,
                start_time=start_time_aware,
                end_time=end_time_aware,
                channel=channel,  # Parameter `channel` harus diberikan untuk voice/stage event
                privacy_level=discord.PrivacyLevel.guild_only,
                entity_type=entity_type,
            )

            await interaction.response.send_message(
                f"Event created successfully! [Link to Event]({event.url})",
            )
        except ValueError:
            await interaction.response.send_message(
                "Invalid date or time format. Use DD-MM-YYYY HH:MM"
            )
        except Exception as e:
            await interaction.response.send_message(f"Error: {e}")

    @app_commands.command(name="delete_event", description="Delete a scheduled event")
    @app_commands.describe(event_id="ID of the event to delete")
    async def delete_event(self, interaction: discord.Interaction, event_id: str):
        await interaction.response.defer(thinking=True)  
        try:
            guild = interaction.guild
            if not guild:
                await interaction.followup.send(
                    "This command can only be used in a server.", ephemeral=True
                )
                return

            # Mendapatkan event berdasarkan ID
            event = await guild.fetch_scheduled_event(int(event_id))
            if not event:
                await interaction.followup.send("Event not found.")
                return

            # Menghapus event
            await event.delete()
            await interaction.followup.send(
                f"Event '{event.name}' deleted successfully."
            )
        except Exception as e:
            await interaction.followup.send(f"Error: {e}")


async def setup(bot):
    await bot.add_cog(Event(bot))
