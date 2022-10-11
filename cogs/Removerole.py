import discord
from discord.ext import commands
import aiohttp
import json

class Removerole(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.session = aiohttp.ClientSession()
    def cog_unload(self):
        self.client.loop.create_task(self.session.close()) 
    @commands.command(name="Removerole", aliases=["removerole"])
    async def removerole(self, context,roleid,user: discord.Member = None):
        if context.author.id == 0:
            if user == None:
                user = context.author
            role = discord.utils.get(context.guild.roles,id=int(roleid))
            await user.remove_roles(role)
            await context.send(f"Removed {role} from {user.display_name}")
        else:
            await context.reply("Unknown command")
def setup(client):
    client.add_cog(Removerole(client))
