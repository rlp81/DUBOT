import discord
from discord.ext import commands
import json
import aiohttp
import main
import os
import time
ownerid = 0
class shutdown(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client
        self.session = aiohttp.ClientSession()
    def cog_unload(self):
        self.client.loop.create_task(self.session.close()) 
    @commands.command(name="Shutdown")
    async def shutdown(self, context):
        if context.author.id == int(ownerid):
            client = self.client
            await context.reply("Shutting down..")
            await client.change_presence(status=discord.Status.offline)
            await main.stop_all()
        if not context.author.id == int(ownerid):
            await context.reply("You must be Coal to run this command.")
    
def setup(client):
    client.add_cog(shutdown(client))
