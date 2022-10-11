from discord.ext import commands
class Ping(commands.Cog):

    def __init__(self, client):
        self.client = client
        import aiohttp
        self.session = aiohttp.ClientSession()
    def cog_unload(self):
        self.client.loop.create_task(self.session.close()) 
    @commands.command(name="Ping", aliases=["ping"])
    async def ping(self, context):
        await context.reply(f"My ping is {round(self.client.latency*1000)}ms")

def setup(client):
    client.add_cog(Ping(client))