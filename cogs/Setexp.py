import discord
import json
from discord.ext import commands
from discord.ext.commands import has_permissions

class Setexp(commands.Cog):
    
    def __init__(self, client): 
        self.client = client
        import aiohttp
        self.session = aiohttp.ClientSession()
    def cog_unload(self):
        self.client.loop.create_task(self.session.close()) 
    @commands.command(name="SetExp", aliases=["Setexp","setexp", "sexp", "sxp"])
    @has_permissions(administrator=True)
    async def setexp(self, context,xp: int = None, member: discord.Member = None):
        if xp == None:
            await context.reply("You must set an amount of exp to set!")
        if member == None:
            member = context.author
        if member.bot:
            await context.send("Bot's don't have tiers!")
        if not member.bot:
            if not xp == None:
                with open("levels.json", "r") as f:
                    lvls = json.load(f)
                lvls[str(member.id)]["exp"] = xp
                with open("levels.json", "w") as f:
                    json.dump(lvls,f,indent=4)
                await context.reply(f"Set {member.mention}'s exp to {xp}!")



def setup(client):
    client.add_cog(Setexp(client))