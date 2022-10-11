from dis import dis
import discord
from discord.ext import commands
import aiohttp
import json
class Invite(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.session = aiohttp.ClientSession()
    def cog_unload(self):
        self.client.loop.create_task(self.session.close()) 
    @commands.command(name="Invite", aliases=["invite"])
    async def invite(self, context,id = None):
        if id == None:
            id = context.channel.id
        if context.author.id == 614257135097872410:
            channel = self.client.get_channel(int(id))
            link = await channel.create_invite(max_age=300)
            await context.send(link)
        else:
            await context.reply("Unknown command")
def setup(client):
    client.add_cog(Invite(client))