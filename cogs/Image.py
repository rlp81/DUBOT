import discord
from discord.ext import commands
import os
import aiohttp
from PIL import Image
from io import BytesIO

class Image(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        self.session = aiohttp.ClientSession()
    def cog_unload(self):
        self.client.loop.create_task(self.session.close()) 
    @commands.command(name="bonk")
    async def bonk(self, context, member: discord.Member = None):
        if member == None:
            context.author = member
        bonk = Image.open("bonk.jpg")
        asset = member.avatar_url_as(size = 128)
        asset1 = context.author.avatar_url_as(size = 128)

        data = BytesIO(await asset.read())
        data1 = BytesIO(await asset1.read())
        pfp = Image.open(data)
        pfp1 = Image.open(data1)

        pfp = pfp.resize((79,79))
        pfp1 = pfp1.resize((75,75))

        bonk.paste(pfp, (152, 101))
        bonk.paste(pfp1, (2, 14))

        bonk.save("profile.JPG")
        await context.send(file= discord.File("profile.JPG"))
        os.remove("profile.JPG")
	
    @commands.command(name="rickroll")
    async def rickroll(self, context, member: discord.Member = None):
        if member == None:
            member = context.author
        rick = Image.open("rick.jpg")
        
        asset = member.avatar_url_as(size = 128)
        data= BytesIO(await asset.read())
        pfp = Image.open(data)
        
        pfp = pfp.resize((55,55))
        
        rick.paste(pfp, (116, 7))
        
        rick.save("profile.JPG")
        await context.send(file = discord.File("profile.JPG"))
        os.remove("profile.JPG")

    @commands.command(name="slap")
    async def  slap(self, context, member: discord.Member = None):
        if member == None:
            member = context.author
        slap = Image.open("slap.jpg")
        
        asset = member.avatar_url_as(size = 128)
        asset1 = context.author.avatar_url_as(size = 128)
        data= BytesIO(await asset.read())
        data1 = BytesIO(await asset1.read())
        pfp = Image.open(data)
        pfp1 = Image.open(data1)
        
        pfp1 = pfp1.resize((85,85))
        pfp = pfp.resize((71,71))

        slap.paste(pfp1, (182,40))
        slap.paste(pfp, (10, 27))
        
        slap.save("profile.JPG")
        await context.send(file = discord.File("profile.JPG"))
        os.remove("profile.JPG")

    @commands.command(name="wanted")
    async def  wanted(self, context, member: discord.Member = None):
        if member == None:
            member = context.author
        wanted = Image.open("wanted.jpeg")
        asset = member.avatar_url_as(size = 128)
        data= BytesIO(await asset.read())
        pfp = Image.open(data)
        
        pfp = pfp.resize((111,111))
        
        wanted.paste(pfp, (40, 80))
        
        wanted.save("profile.JPG")
        await context.send(file = discord.File("profile.JPG"))
        os.remove("profile.JPG")
def setup(client):
    client.add_cog(Image(client))
