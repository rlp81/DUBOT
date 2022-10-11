import discord
from discord.ext import commands
import aiohttp
from discord.ext.commands import has_permissions
class UnMute(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        self.session = aiohttp.ClientSession()
    def cog_unload(self):
        self.client.loop.create_task(self.session.close())     
    @commands.command(name="UnMute")
    @has_permissions(manage_messages=True)
    async def UnMute(self, context, member: discord.Member):
        role = discord.utils.get(context.guild.roles, name="Muted")
        try:
            await member.remove_roles(role)
            await context.message.add_reaction("✅")
            await context.send(f"I have unmuted {member}.")
            try:
                await member.send(f"{context.author} unmuted you.")
            except:
                await context.reply(f"{member} has their dms closed.")
        except:
            await context.reply(f"Failed to unmute {member.display_name}.")

def setup(client):
    client.add_cog(UnMute(client))
