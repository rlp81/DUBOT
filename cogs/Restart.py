import discord
from discord.ext import commands
import json
import aiohttp
import os
import time
import sys
ownerid = 0
def restart_bot(): 
    os.execv(sys.executable, ['python3.9'] + sys.argv)
class Restart(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.session = aiohttp.ClientSession()
    def cog_unload(self):
        self.client.loop.create_task(self.session.close()) 
    @commands.command(name="Restart")
    async def restart(self, context):
        if context.author.id == int(ownerid):
            await context.reply("Restarting bot..")
            restart_bot()
        if not context.author.id == int(ownerid):
            await context.reply("You must be Coal to run this command.")
    
def setup(client):
    client.add_cog(Restart(client))
