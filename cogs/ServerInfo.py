import discord
from discord.ext import commands
import aiohttp
from discord.ext.commands import has_permissions
def get_bots(server: discord.Guild):
    bots = 0
    for i in server.members:
        if i.bot:
            bots += 1
    return bots
class ServerInfo(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        self.session = aiohttp.ClientSession()
    def cog_unload(self):
        self.client.loop.create_task(self.session.close()) 
    @commands.command(name='ServerInfo', pass_context = True, aliases=['serverinfo', 'Serverinfo', 'SERVERINFO'])
    async def serverinfo(self, context):
        server: discord.Guild = context.guild
        em = discord.Embed(title="ServerInfo", description=server.name)
        em.add_field(name="ID", value=server.id)
        em.add_field(name="Server made in", value=server.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
        em.add_field(name="Server members", value=server.member_count)
        em.add_field(name="Bots", value=get_bots(server))
        em.add_field(name="Requested by", value=context.author)
        em.set_thumbnail(url=server.icon_url)
        await context.reply(embed=em)

def setup(client):
    client.add_cog(ServerInfo(client))