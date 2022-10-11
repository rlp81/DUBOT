from email import message
import os
import discord
import aiohttp
from discord import client
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont

class Img(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.session = aiohttp.ClientSession()
    def cog_unload(self):
        self.client.loop.create_task(self.session.close()) 
    @commands.command(name="Img")
    async def Img(self, context,member: discord.Member):
        W, H = (438,259)
        img = Image.open("welcome.png", "r")
        await member.avatar.save("pfp.png")
        img2 = Image.open("pfp.png", "r")
        img.paste(img2,(157,22))
        img1 = Image.open("welcome1.png", "r")
        draw = ImageDraw.Draw(img1)
        font = ImageFont.truetype("arial.ttf", 25)
        w, h = draw.textsize(str(member))
        draw.text(((W-w)/2-30,180), str(member), (0, 0, 0), font=font)
        bg = Image.new("RGBA",(W,H), (0,0,0,0))
        bg.paste(img, (0,0))
        bg.paste(img1, (0,0), mask=img1)
        bg.save("image.png",format="png")
        await context.send(file=discord.File("image.png"))
        os.remove("image.png")
def setup(client):
    client.add_cog(Img(client))