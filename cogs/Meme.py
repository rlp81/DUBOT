import discord
from discord.ext import commands
import os
import random
from discord.ext.commands import has_permissions
from discord.flags import MessageFlags

class Meme(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        import aiohttp
        self.session = aiohttp.ClientSession()
    def cog_unload(self):
        self.client.loop.create_task(self.session.close()) 
    @commands.command(name="memes")
    async def memes(self, context):
        bans = [818939178661838868]
        if not context.author.id in bans:
            lis = ""
            num = 0
            files = os.listdir("./memes")
            for file in sorted(files):
                lis += f"{file}\n"
                num += 1
            try:
                file = f"Memes in database: {num}\n{lis}"
                path = os.getcwd()
                with open("memes.txt","w") as f:
                    f.write(file)
                location = f"{path}/"+"memes.txt"
                await context.send(file=discord.File(location))
            except:
                await context.send("An error occured sending you the meme database.")
    @commands.command(name="meme")
    async def meme(self, context, message = None):
        bans = [818939178661838868]
        if not context.author.id in bans:
            if not message == None:
                files = os.listdir("./memes")
                finfile = None
                for file in files:
                    lowfile = file.lower()
                    message = message.lower()
                    if message in lowfile:
                        finfile = file
                        break
                if finfile == None:
                    await context.reply(f"Could not find a file with {message}")
                if not finfile == None:
                    path = os.getcwd()
                    location = f"{path}/memes/"+file
                    await context.send("Sending file..")
                    async with context.typing():
                        try:
                            await context.send(file=discord.File(location))
                        except:
                            await context.reply(f"An error occured sending {finfile}")
            if message == None:
                file = random.choice(os.listdir("./memes"))
                finfile = file
                path = os.getcwd()
                location = f"{path}/memes/"+file
                await context.send("Sending file..")
                async with context.typing():
                    try:
                        await context.send(file=discord.File(location))
                    except:
                        await context.reply(f"An error occured sending {finfile}")            

def setup(client):
    client.add_cog(Meme(client))
