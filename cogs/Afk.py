import discord
from discord import Member, client
from discord.ext import commands
import aiohttp
import json

class Afk(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.session = aiohttp.ClientSession()
    def cog_unload(self):
        self.client.loop.create_task(self.session.close()) 
    @commands.command(name="Afk", aliases=["afk"])
    async def afk(self, context):
        with open("afk.json", "r") as f:
            af = json.load(f)
        id = context.author.id
        disp = context.author.display_name
        af[id] = disp
        with open("afk.json", "w") as f:
            json.dump(af,f)
        name = f"[AFK]{disp}"
        try:
            await context.author.edit(nick=name)
            await context.send("Set you AFK!")
        except:
            await context.reply("I do not have the correct permissions to change your nickname.")
def setup(client):
    client.add_cog(Afk(client))