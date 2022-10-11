import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.ext.commands.core import guild_only
class Mute(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        import aiohttp
        self.session = aiohttp.ClientSession()
    def cog_unload(self):
        self.client.loop.create_task(self.session.close()) 
    @commands.command(name="Mute", aliases=["mute"])
    @has_permissions(manage_messages=True)
    async def Mute(self, context, member: discord.Member,*,message):
        role = discord.utils.get(context.guild.roles, name="Muted")
        try:
            await member.add_roles(role)
            await context.message.add_reaction("?")
            await context.send(f"I have muted {member} for {message}.")
            try:
                await member.send(f"{context.author} muted you for {message}.")
            except:
                await context.reply(f"{member} has their dms closed.")
        except:
            await context.reply(f"Failed to mute {member.display_name}.")
    @commands.command(name="TempMute", aliases=["tempmute", "tmute", "TMute", "Tmute"])
    @has_permissions(manage_messages=True)
    async def TempMute(self, context, member: discord.Member,time,*,message):
        role = discord.utils.get(context.guild.roles, name="Muted")
        try:
            await member.add_roles(role)
            await context.reply(f"I have muted {member} for {message} for {time} seconds.")
            try:
                await member.send(f"{context.author} muted you for {message} for {time} seconds.")
            except:
                await context.reply(f"{member} has their dms closed.")
            await asyncio.sleep(int(time))
            try:
                await member.remove_roles(role)
                await context.reply(f"I have unmuted {member} because they have servered their time.")
            except:
                await context.reply(f"Could not unmute {member}.")
        except:
            await context.reply(f"Failed to mute {member.display_name}.")

def setup(client):
    client.add_cog(Mute(client))
