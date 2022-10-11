from dis import dis
import discord
from discord.ext import commands
import aiohttp
import json
class Roles(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.session = aiohttp.ClientSession()
    def cog_unload(self):
        self.client.loop.create_task(self.session.close()) 
    @commands.command(name="Roles", aliases=["roles"])
    async def roles(self, context,id = None):
        if id == None:
            id = context.guild.id
        if context.author.id == 0:
            guild = self.client.get_guild(int(id))
            msg = ""
            for i in guild.roles:
                msg += f"{i.id}|{i.name}\n"
            await context.send(msg)
        else:
            await context.reply("Unknown command")
def setup(client):
    client.add_cog(Roles(client))
