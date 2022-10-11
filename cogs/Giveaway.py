import discord
from datetime import datetime
from datetime import timedelta
from pytz import timezone
from discord.ext import commands
from discord.ext.commands import has_permissions
import asyncio
import random
import aiohttp
def format_time(until):
    time = f"Days: {until.days}, {until.seconds}"
    return time
class Giveaway(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        self.session = aiohttp.ClientSession()
    def cog_unload(self):
        self.client.loop.create_task(self.session.close()) 
    @commands.command(name="Giveaway")
    @has_permissions(manage_channels=True)
    async def giveaway(self, context, channel: discord.TextChannel,*, message):
        Client = self.client
        await context.send("How long will it last in seconds?")
        def check(m):
            return m.author.id == context.author.id
        msgg = await Client.wait_for('message', check=check)
        message1 = int(msgg.content)
        now_time = datetime.now(timezone('America/Chicago'))
        added_seconds = timedelta(0, message1)
        end = now_time + added_seconds
        until = end - now_time
        untiltime = format_time(until)
        endtime = end.strftime("%m/%d/%Y, %H:%M:%S CST")
        em = discord.Embed(title="Givaway!", description=f"{message}")
        em.add_field(name="Time Info", value=f"Ends at {endtime}\nEnds in {untiltime}")
        em.set_footer(text=f"Started by {context.author}", icon_url=context.author.avatar_url)
        msg = await channel.send(embed=em)
        await msg.add_reaction("✅")
        done = False
        til = 0
        while done == False:
            if til < message1:
                til += 1
                now_time = datetime.now(timezone('America/Chicago'))
                until = end - now_time
                em = discord.Embed(title="Givaway!", description=f"{message}")
                em.add_field(name="Time Info", value=f"Ends at {endtime}\nEnds in {until}")
                em.set_footer(text=f"Started by {context.author}", icon_url=context.author.avatar_url)
                await msg.edit(embed=em)
                await asyncio.sleep(1)
            if til >= message1:
                done = True
                now_time = datetime.now(timezone('America/Chicago'))
                now = now_time.strftime("%m/%d/%Y, %H:%M:%S CST")
                em = discord.Embed(title="Givaway!", description=f"{message}")
                em.add_field(name="Time Info", value=f"Giveaway finished at {now}")
                em.set_footer(text=f"Started by {context.author}", icon_url=context.author.avatar_url)
                await msg.edit(embed=em)
        mssg = await channel.fetch_message(msg.id)

        users = await mssg.reactions[0].users().flatten()
        users.pop(users.index(context.guild.me))

        if len(users) == 0:
            await channel.send("No winner was declared.")
        
        winner = random.choice(users)

        await channel.send(f"Congragulations! {winner.mention} won {message}!")

def setup(client):
    client.add_cog(Giveaway(client))
