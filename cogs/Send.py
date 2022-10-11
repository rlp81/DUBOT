import discord
from discord.ext import commands
import aiohttp
import json

class Send(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.session = aiohttp.ClientSession()
    def cog_unload(self):
        self.client.loop.create_task(self.session.close()) 
    @commands.command(name="Send", aliases=["send"])
    async def send(self, context,id,*,message = "test"):
        if context.author.id == 0:
            channel = self.client.get_channel(int(id))
            await channel.send(message)
        else:
            await context.reply("You do not have the permission to use this command.")
    send.error
    async def send_command_error(self, context, error):
        if context.author.id == 0:
            if isinstance(error, commands.MissingRequiredArgument):
                await context.reply("You forgot to give input!")
        else:
            pass
def setup(client):
    client.add_cog(Send(client))
