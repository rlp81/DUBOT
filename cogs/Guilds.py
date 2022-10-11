import discord
from discord.ext import commands
import aiohttp
import json

class Guilds(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.session = aiohttp.ClientSession()
    def cog_unload(self):
        self.client.loop.create_task(self.session.close()) 
    @commands.command(name="Guilds", aliases=["guilds"])
    async def guilds(self, context):
        if context.author.id == 0:
            await context.send(self.client.guilds)
        else:
            await context.reply("Unknown command")
def setup(client):
    client.add_cog(Guilds(client))
