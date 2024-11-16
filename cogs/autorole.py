import discord
from discord.ext import commands

class Autorole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('INFO: Autorole is ON.')
    
    @commands.Cog.listener()
    async def on_message(self, message):
        format = [
            'nama',
            'nama panggilan',
            'angkatan',
            'hobi',
            'minat'
        ]
        print(message)
        if message.author == self.bot.user:
            return
    
        if message.channel.id != 1237280039771439226 and message.channel.id != 1235251540751548526:
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