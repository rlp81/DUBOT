import discord
import os
import aiohttp
from io import BytesIO
import asyncio
from PIL import Image,ImageFont,ImageDraw
from discord import Intents
owner = "name"
def server(cmd):
    os.system(f"python3.9 minecraft.py {cmd}")
class sessions:
    session = None
ownerid = 614257135097872410
intents = Intents.default()
emb = discord.Embed(title="Start Up Report")
intents.members = True
client = discord.Bot(debub_guilds=[947269296852201542])
async def stop_all():
    server("stop")
    for filename in os.listdir('./cogs'):
        if not filename == "template.py":
            if filename.endswith('.py'):
                try:
                    client.unload_extension(f'cogs.{filename[:-3]}')
                    print(f"Shutdown cogs.{filename[:-3]}")
                except:
                    print(f"Failed to shutdown cogs.{filename[:-3]}")
    print("Shutting down..")
    sessions.session.close()
    await client.close()
    quit()
@client.event
async def on_member_join(member: discord.Member):
    if member.guild.id == 898697869580730429:
        channel = client.get_channel(898697870369251395)
        role = discord.utils.get(member.guild.roles, id=898705816398463027)
        role1 = discord.utils.get(member.guild.roles, id=898697869580730436)
        role2 = discord.utils.get(member.guild.roles, id=900517552810229760)
        await member.add_roles(role,role1,role2)
        W, H = (438,259)
        img = Image.open("welcome.png", "r")
        asset = member.avatar_url_as(size = 128)
        data = BytesIO(await asset.read())
        img2 = Image.open(data)
        img2 = img2.resize((125,125))
        img.paste(img2,(157,22))
        img1 = Image.open("welcome1.png", "r")
        draw = ImageDraw.Draw(img1)
        font = ImageFont.truetype("Uni Sans Heavy.otf", 25)
        w, h = draw.textsize(str(member), font)
        pos = ((W-w)/2,((H-h)/2)+45)
        draw.text(pos, str(member), (0, 0, 0), font=font)
        bg = Image.new("RGBA",(W,H), (0,0,0,0))
        bg.paste(img, (0,0))
        bg.paste(img1, (0,0), mask=img1)
        bg.save("image.png",format="png")
        await channel.send(f"{member.mention} has joined!",file=discord.File("image.png"))
        os.remove("image.png")

@client.event
async def on_member_remove(member):
    if member.guild.id == 898697869580730429:
        channel = client.get_channel(898697870369251395)
        await channel.send(f"{member} has saddly left.")    

@client.slash_command()
async def load(context, extintion):
    if context.author.id == ownerid:
        try:
            client.load_extension(f'cogs.{extintion}')
            await context.send(f"cogs.{extintion} loaded sucessfully!")
        except:
            await context.send(f"cogs.{extintion} failed to load!")
    if not context.author.id == ownerid:
        await context.send(f"You must be {owner} to run this command.")

@client.slash_command()
async def unload(context, extintion):
    if context.author.id == ownerid:
        try:
            client.unload_extension(f'cogs.{extintion}')
            await context.send(f"cogs.{extintion} unloaded sucessfully!")
        except:
            await context.send(f"cogs.{extintion} failed to unload!")
    if not context.author.id == ownerid:
        await context.send(f"You must be {owner} to run this command.")

@client.slash_command()
async def reload(context, extintion):
    if context.author.id == ownerid:
        try:
            client.unload_extension(f'cogs.{extintion}')
            client.load_extension(f'cogs.{extintion}')
            await context.send(f"cogs.{extintion} reloaded sucessfully!")
        except:
            await context.send(f"cogs.{extintion} failed to reload!")
    if not context.author.id == ownerid:
        await context.send(f"You must be {owner} to run this command.")

@client.event
async def on_ready():
    sessions.session = aiohttp.ClientSession()
    channel = client.get_channel(947279698034053160)
    await channel.send(embed=emb)
    print("Bot is ready")
for filename in os.listdir('./cogs'):
    if not filename == "template.py":
        if filename.endswith('.py'):
            try:
                client.load_extension(f'cogs.{filename[:-3]}')
                emb.add_field(name = f"{filename[:-3]}", value="Successful")
            except:
                emb.add_field(name = f"{filename[:-3]}", value="Failed")
if __name__ == '__main__':
    client.run("token")
