import json
import discord
from discord.ext import commands
import asyncio
from datetime import datetime
import random
import requests
import os
mostact = 0 #role id
coin = "" #emoji example: <:coin:12345>
guilds = [0]
class dones:
    done = False
    used = False
th = False
blacklisted = ["nigger","nigga","niger","niga","nniiggeerr","nniiggggeerr","nniiggaa"]#,"owo","uwu","^w^","'w'","nwn","vwv","xwx",":3","3:","$w$","*w*","TwT","ewe"]
async def send_message(self, msg):
    content = f"||{msg.channel.id}||\n{msg.guild}/{msg.channel}|{msg.author}: {msg.content}"
    channel = self.client.get_channel(0)
    if msg.attachments:
        for url in msg.attachments:
            r = requests.get(url, allow_redirects=True)
            name = r.headers['content-type']
            if "/" in name:
                name = name.replace("/",".")
            if "video" in name:
                if "quicktime" in name:
                    name = name.replace("quicktime","mp4")
            with open(name,"wb") as f:
                f.write(r.content)
        await channel.send(content,file=discord.File(f"{os.getcwd()}/{name}"))
        os.remove(f"{os.getcwd()}/{name}")
    else:
        await channel.send(content)
def Convert(string):
    list1=[]
    list1[:0]=string
    return list1
async def check_if_mostactive(client: commands.Bot, message: discord.Message):
    with open("levels.json","r") as f:
        levels: dict = json.load(f)
    role = discord.utils.get(message.guild.roles,id=0)
    best = 0
    bestusr = 0
    for key,value in levels.items():
        id = int(key)
        exp = int(levels[key]["exp"])
        if exp > best:
            best = exp
            bestusr = id
    for member in message.guild.members:
        if member.id == bestusr:
            user = member
            break
    await user.add_roles(role)
async def check_if_afk(message: discord.Message):
    if message.author.display_name.startswith("[AFK]"):
        with open("afk.json", "r") as f:
            af: dict = json.load(f)
        if af[str(message.author.id)]:
            nick: str = af[str(message.author.id)]
            await message.author.edit(nick=nick)
            af.pop(str(message.author.id))
            with open("afk.json", "w") as f:
                json.dump(af,f)
            await message.channel.send(f"Welcome back, {message.author.display_name}!")
            if nick.startswith("[AFK]"):
                await message.author.edit(nick=message.author.name)
async def check_if_afk_ping(message: discord.Message):
    with open("afk.json", "r") as f:
        af: dict = json.load(f)
    userid = None
    for name,value in af.items():
        if name in message.content:
            userid = name
            break
    if userid != None:
        if f"<@!{userid}>" in message.content:
            member = af[userid]
            await message.reply(f"Please do not bother {member} at this time.")
async def countdown():
    time = 1200
    while dones.done == False:
        time -= 1
        await asyncio.sleep(1)
        if time <= 0:
            dones.done = True

async def question():
    opts = ["math","scramble","word"]
    opt = random.choice(opts)
    if opt == "scramble":
        words = ["dubengar","youtube","science","programming","gaming","video","gamer","roblox","discord","funny","steam"]
        word = random.choice(words)
        wordl = Convert(word)
        random.shuffle(wordl)
        newword = ""
        for item in wordl:
            newword += item
        ques = f"Unscrabble the word: {newword}"
        return (ques, word)
    if opt == "math":
        nums = [1,2,3,4,5,6,7,8,9,10]
        num1 = random.choice(nums)
        num2 = random.choice(nums)
        sym = random.choice(["+","-","/","*"])
        global ans
        if sym == "+":
            ans = num1+num2
        if sym == "-":
            ans = num1-num2
        if sym == "*":
            ans = num1*num2
        if sym == "/":
            ans = num1/num2
        ques = f"What is {num1}{sym}{num2}?"
        return (ques,str(ans))
    if opt == "word":
        ready = False
        words = ["dubengar","youtube","science","programming","gaming","video","gamer","roblox","discord","funny","steam"]
        while ready == False:
            word = random.choice(words)
            wordl = Convert(word)
            chars = 0
            for i in wordl:
                chars += 1
            num = random.randint(2,4)
            if num < chars-3:
                ready = True
                await asyncio.sleep(.01)
            else:
                await asyncio.sleep(.01)
        for i in range(num):
            got = False
            while got == False:
                rem = random.choice(wordl)
                if not rem == "_":
                    wordl[rem] = "_"
                    got = True
                await asyncio.sleep(.01)
        newword = ""
        for i in wordl:
            newword += i
        ques = f"Spell the word: {newword}"
        return (ques, word)

async def guesswhat(self, used):
    if used == False:
        used = True
        await countdown()
        while dones.done == False:
            await asyncio.sleep(.01)
            if dones.done == True:
                channel = self.client.get_channel(0)
                ques, ans = await question()
                await channel.send(ques)
                msg = await self.client.wait_for('message')
                msgg = msg.content
                if msgg == ans:
                    prize = random.randint(50,100)
                    await msg.send(f"{msg.author} answered correctlys first and won {prize}{coin}!")
                    with open("wallet.json","r") as f:
                        wal = json.load(f)
                    wal[str(msg.author.id)]["money"] = int(wal[str(msg.author.id)]["money"]) + prize
                else:
                    await msg.reply("Incorrect!")
                dones.done = False
            
async def mute(msg):
    angel = discord.utils.get(msg.guild.roles, id=0)
    muted = discord.utils.get(msg.guild.roles, id=0)
    await msg.author.remove_roles(angel)
    await msg.author.add_roles(muted)
    await asyncio.sleep(3600)
    await msg.author.remove_roles(muted)
    await msg.author.add_roles(angel)

async def spamdetect(msg):
    counter = 0
    counter1 = 0
    with open("spam_detect.txt", "r+") as f:
        for lines in f:
            if lines.strip("\n") == str(msg.author.id):
                counter+=1
        f.writelines(f"{str(msg.author.id)}\n")
        if counter >= 4:
            await msg.channel.send(f"Stop spamming {msg.author.mention}!")
            with open("spam_warns.txt", "r+") as fi:
                for lines in fi:
                    if lines.strip("\n") == str(msg.author.id):
                        counter1+=1
                fi.writelines(f"{str(msg.author.id)}\n")
                if counter1 >= 6:
                    await mute(msg)
                if counter1 >= 12:
                    await msg.author.ban(reason="spam")


async def blacklist(message):
    for word in blacklisted:
        if word in str(message).lower():
            await message.delete()
            await message.channel.send(f"{message.author.mention} that is a blacklisted word!")

roles = {10:0,20:1,30:2,40:3,50:4,60:5,70:6,80:7,90:8,100:9}
async def add_roles(self, level,user,channel):
    if not user == self.client.user:
        levels = roles.keys()
        for lvl in levels:
            if level >= lvl:
                name = int(roles[lvl])
                role = discord.utils.get(channel.guild.roles, id=name)
                if not role in user.roles:
                    if channel.guild.id == 0:
                        await user.add_roles(role)
async def update_data(self, users, user):
    if not user == self.client.user:
        if not str(user.id) in str(users):
            users[user.id] = {} 
            users[user.id]["exp"] = 0
            users[user.id]["level"] = 1
        with open("levels.json", "w") as f:
                json.dump(users, f, indent=4)
async def add_exp(self, users, user, exp, channel):
    if not user == self.client.user:
        users[str(user.id)]["exp"] = int(users[str(user.id)]["exp"]) + int(exp)
        await add_roles(self, int(users[str(user.id)]["level"]), user, channel)
async def level_up(self, users, user):
    if not user == self.client.user:
        exp = users[str(user.id)]["exp"]
        lvlstart = users[str(user.id)]["level"]
        lvlend = int(exp ** (1/4))
        if lvlstart < lvlend:
            lvlchan = self.client.get_channel(0)
            await lvlchan.send(f"{user.mention} has leveled up to tier {lvlend}!")
            users[str(user.id)]["level"] = lvlend
            with open("levels.json", "w") as f:
                json.dump(users, f, indent=4)
class emojis:
        check = "?"
        xcheck = "?"
class on_message(commands.Cog):
    def __init__(self, client):
        self.client = client
        import aiohttp
        self.session = aiohttp.ClientSession()
    def cog_unload(self):
        self.client.loop.create_task(self.session.close()) 
    @commands.Cog.listener()
    async def on_message(self, message):
        if str(message.channel.type) == 'private':
            if not message.author == self.client.user:
                channel = self.client.get_channel(0)
                #await channel.send(f"**New ModMail!**\n{message.author}:{message.content}")
        if message.guild.id in guilds:
            await send_message(self,message)
            await check_if_afk(message)
            await check_if_afk_ping(message) 
            await blacklist(message)
            #if not message.author == self.client.user:
                #await spamdetect(message)
            with open('wallet.json', 'r') as f:
                wal = json.load(f)
            with open('bank.json', 'r') as f:
                bank = json.load(f)
            with open("inv.json", "r") as f:
                inv = json.load(f)
            if not str(message.author.id) in inv:
                inv[message.author.id] = {}
                with open('inv.json', 'w') as f:
                    json.dump(inv,f,indent=4)
            if not str(message.author.id) in wal:
                wal[message.author.id] = {}
                wal[message.author.id]["name"] = str(message.author)
                wal[message.author.id]["money"] = 1
                with open('wallet.json', 'w') as f:
                    json.dump(wal,f,indent=4)
            if not str(message.author.id) in bank:
                bank[message.author.id] = {}
                bank[message.author.id]["name"] = str(message.author)
                bank[message.author.id]["money"] = 0
                with open('bank.json', 'w') as f:
                    json.dump(bank,f,indent=4)
            #if wal[str(message.author.id)]["money"] < str(0):
                #wal[str(message.author.id)]["money"] = 0
                #with open("wallet.json", "w") as f:
                    #json.dump(wal,f,indent=4)
            wal[str(message.author.id)][str("money")] = int(wal[str(message.author.id)]["money"]) + 1
            with open("wallet.json", "w") as f:
                json.dump(wal,f,indent=4)
            with open("levels.json", "r") as f:
                levels = json.load(f)
            await update_data(self, levels, message.author)
            await add_exp(self, levels, message.author, 30, message.channel)
            await level_up(self, levels, message.author)
            #await check_if_mostactive(self.client,message)
            with open("levels.json", "w") as f:
                json.dump(levels, f, indent=4)
            await guesswhat(self,used=dones.used)
            #await self.client.process_commands(message)
def setup(client):
    client.add_cog(on_message(client))
