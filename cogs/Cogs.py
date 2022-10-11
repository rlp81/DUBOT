import discord
from discord.ext import commands
import os

class Cogs(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
    def cog_unload(self):
        self.client.loop.create_task(self.session.close()) 
    @commands.command(name="Cogs", aliases=["cogs"])
    async def cogs(self, context):
        files = os.listdir("./cogs")
        names = ""
        for file in files:
            names += f"{file}\n"
        await context.reply(names)
def setup(client):
    client.add_cog(Cogs(client))
