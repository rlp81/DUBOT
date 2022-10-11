import discord
from discord.ext import commands
import wolframalpha
import random
import aiohttp
app = "appi-id"
wolfclient = wolframalpha.Client(app)
colors = [0xff0006,0x00ff20,0x0e2aaa,0x00cfff,0x00470f,0xff00f3,0x020353,0xffe49a,0xffff00,0x00ff74]
class AI(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        self.session = aiohttp.ClientSession()
    def cog_unload(self):
        self.client.loop.create_task(self.session.close()) 
    @commands.command(name="AI",aliases=["ai","ask","Ask"])
    async def ai(self,context,*,message):
        async with context.typing():
            try:
                res = wolfclient.query(message)
                answer = next(res.results).text
                emb=discord.Embed(title=answer,color=random.choice(colors))
                emb.set_footer(text="Wolfram Alpha AI :D",icon_url="https://cdn.discordapp.com/attachments/898697869941428319/912816005263286382/unknown.png")
                await context.reply(embed=emb)
            except:
                await context.reply("Critical Error")
        

def setup(client):
    client.add_cog(AI(client))
