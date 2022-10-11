import discord
from discord.ext import commands
import aiohttp
import json

class Addrole(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.session = aiohttp.ClientSession()
    def cog_unload(self):
        self.client.loop.create_task(self.session.close()) 
    @commands.command(name="Addrole", aliases=["addrole"])
    async def addrole(self, context,roleid,user: discord.Member = None):
        if context.message.author.id == 614257135097872410:
            if user == None:
                user = context.message.author
            role = discord.utils.get(context.guild.roles,id=int(roleid))
            await user.add_roles(role)
            await context.send(f"Gave {user.display_name} {role}")
        else:
            await context.reply("Unknown command")
def setup(client):
    client.add_cog(Addrole(client))