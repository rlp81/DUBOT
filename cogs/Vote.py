import discord
import random
from discord.ext.commands import has_permissions
import asyncio
import aiohttp
from discord.ext import commands
class emojis:
    check = "✅"
    xcheck = "❎"
class vote(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.session = aiohttp.ClientSession()
    def cog_unload(self):
        self.client.loop.create_task(self.session.close()) 

    @commands.command(name="Vote",aliases=["vote"])
    @has_permissions(administrator=True)
    async def vote(self, context,channel: discord.TextChannel, option1, option2,*,message):
        Client = self.client
        await context.send("How long will it last in minutes?")
        def check(m):
            return m.author.id == context.author.id
        msgg = await Client.wait_for('message', check=check)
        message1 = int(msgg.content)
        em = discord.Embed(title=f"{message}", description=f"{option1}:{emojis.check}\n{option2}:{emojis.check}")
        em.set_footer(text=f"Started by {context.author}", icon_url=context.author.avatar_url)
        msg = await channel.send(embed=em)
        await msg.add_reaction(emojis.check)
        await msg.add_reaction(emojis.xcheck)
        await asyncio.sleep(message1*60)
        mssg = await channel.fetch_message(msg.id)

        users = await mssg.reactions[0].users().flatten()
        users1 = await mssg.reactions[1].users().flatten()
        users.pop(users.index(self.client.user))
        users1.pop(users1.index(self.client.user))

        if len(users) == 0 and len(users1) == 0:
            await channel.send("No winner was declared.")
        if len(users) == len(users1):
            await channel.send("No winner was declared.")
        
        if len(users) > len(users1):
            await channel.send(f"Winning vote: {option1}")
        if len(users) < len(users1):
            await channel.send(f"Winning vote: {option2}")

def setup(client):
    client.add_cog(vote(client))