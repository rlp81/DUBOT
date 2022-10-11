import discord
from discord.ext import commands
import aiohttp
from discord.ext.commands import has_permissions

class UserInfo(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        self.session = aiohttp.ClientSession()
    def cog_unload(self):
        self.client.loop.create_task(self.session.close()) 
    @commands.command(name='UserInfo', pass_context = True, aliases=['userinfo', 'Userinfo', 'USERINFO'])
    async def UserInfo(self, context, member: discord.Member = None):
        if member == None:
            member = context.author
        em = discord.Embed(title="UserInfo", description=member.display_name)
        em.add_field(name="ID", value=member.id)
        em.add_field(name="account made in", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
        em.add_field(name="account joined server", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
        em.add_field(name="Requested by", value=context.author)
        em.set_thumbnail(url=member.avatar_url)
        await context.reply(embed=em)

def setup(client):
    client.add_cog(UserInfo(client))