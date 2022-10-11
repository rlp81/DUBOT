from dis import dis
import discord
import json
from discord.ext import commands
from discord.ext.commands import has_permissions

class Level(commands.Cog):
    
    def __init__(self, client): 
        self.client = client
        import aiohttp
        self.session = aiohttp.ClientSession()
    def cog_unload(self):
        self.client.loop.create_task(self.session.close()) 
    @commands.command(name="Level", aliases=["level", "lev", "Lev", "Tier", "tier"])
    async def level(self, context: commands.Context, member: discord.Member = None):
        if member == None:
            member = context.author
        if member.bot:
            await context.send("Bot's don't have tiers!")
        if not member.bot:
            with open("levels.json", "r") as f:
                lvls = json.load(f)
            exp = lvls[str(member.id)]["exp"]
            level = lvls[str(member.id)]["level"]
            next_level = int(level)+1
            messages = round(int(exp)/30)
            emb = discord.Embed(
                title=f"({member.display_name}){member}'s Tier",
                description=f"Tier: {level}\nNext Tier: {next_level}\nExp: {exp}\nMessages sent: {messages}"
                )
            avatar = None
            if member.avatar_url:
                avatar = member.avatar_url
            else:
                avatar = member.guild_avatar.url
            emb.set_thumbnail(url=avatar)
            await context.reply(embed=emb)

def setup(client):
    client.add_cog(Level(client))