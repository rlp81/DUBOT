import asyncio
import discord
from discord.ext import commands
import aiohttp
import json
import requests
import os
class Sendfile(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.session = aiohttp.ClientSession()
    def cog_unload(self):
        self.client.loop.create_task(self.session.close()) 
    @commands.command(name="Sendfile", aliases=["sendfile"])
    async def sendfile(self, context,id):
        if context.author.id == 0:
            channel = self.client.get_channel(int(id))
            url = context.message.attachments[0].url
            r = requests.get(url, allow_redirects=True)
            name = r.headers['content-type']
            if "/" in name:
                name = name.replace("/",".")
            if "video" in name:
                if "quicktime" in name:
                    name = name.replace("quicktime","mp4")
            with open(name,"wb") as f:
                f.write(r.content)
            await channel.send(file=discord.File(f"{os.getcwd()}/{name}"))
            os.remove(f"{os.getcwd()}/{name}")
        else:
            await context.reply("You do not have the permission to use this command.")
def setup(client):
    client.add_cog(Sendfile(client))
