import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import asyncio
import aiohttp

class Clear(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        self.session = aiohttp.ClientSession()
    def cog_unload(self):
        self.client.loop.create_task(self.session.close()) 
    @commands.command(name="Clear", aliases=["clear", "Purge", "purge"])
    @has_permissions(manage_messages=True)
    async def Clear(self,context,message):
        await context.message.delete()
        await context.channel.purge(limit=int(message))
        msg = await context.send(f"Successfully purged {message} messages!")
        await asyncio.sleep(5)
        await msg.delete()
def setup(client):
    client.add_cog(Clear(client))