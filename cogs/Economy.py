import discord
import json
import asyncio
from discord.ext import commands
from discord.ext.commands import has_permissions, BucketType, cooldown
import random
import aiohttp
owners = [0]
special = [0]
coin = "<:spiritshard:899139250656784384>"
def sort_json(file, ID):
    try:
        return int(file[ID]['money'])
    except KeyError:
        return 0

class Economy(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        self.session = aiohttp.ClientSession()
    def cog_unload(self):
        self.client.loop.create_task(self.session.close()) 
    @commands.command(name="Balance", aliases=["balance", "bal", "Bal"])
    async def money(self, context, member: discord.Member = None):
        if member == None:
            member = context.author
        with open("bank.json", "r") as f:
            bank = json.load(f)
        with open("wallet.json", "r") as f:
            wallet = json.load(f)
        wal = wallet[str(member.id)]["money"]
        ban = bank[str(member.id)]["money"]
        emb = discord.Embed(title=f"{member.display_name}'s Balance", description=f"Wallet: {wal}{coin}\nBank: {ban}{coin}")
        await context.reply(embed=emb)
    @commands.command(name="Sell", aliases=["sell"])
    async def sell(self, context, item):
        if item != None:
            with open("wallet.json","r") as f:
                wal = json.load(f)
            with open("inv.json", "r") as f:
                inv = json.load(f)
            if item == "all":
                value = 0
                items = []
                for i,v in inv[str(context.author.id)].items():
                    if inv[str(context.author.id)][i]["settings"]["sellable"] == "true":
                        price = inv[str(context.author.id)][i]["value"]
                        value += price
                        items.insert(1,i)
                        wal[str(context.author.id)]["money"] = wal[str(context.author.id)]["money"] + price
                for i in items:
                    inv[str(context.author.id)].pop(i)
                with open("inv.json", "w") as f:
                    json.dump(inv, f,indent=4)
                with open("wallet.json", "w") as f:
                    json.dump(wal, f, indent=4)
                await context.reply(f"You sold all your items for {value}{coin}!")
            else:
                if item in inv[str(context.author.id)]:
                    if inv[str(context.author.id)][item]["settings"]["sellable"] == "true":
                        sellable = inv[str(context.author.id)][item]
                        value = sellable["value"]
                        name = inv[str(context.author.id)][item]["name"]
                        bal = wal[str(context.author.id)]["money"] + value
                        wal[str(context.author.id)]["money"] = bal
                        inv[str(context.author.id)].pop(item)
                        with open("wallet.json", "w") as f:
                            json.dump(wal, f,indent=4)
                        with open("inv.json", "w") as f:
                            json.dump(inv, f, indent=4)
                        await context.reply(f"Successfully sold {name} for {value}{coin}!")
                    else:
                        await context.reply("Item not sellable.")
                else:
                    await context.reply("You do not have this item in your inventory!")
        else:
            await context.reply("You did not give an item to sell!")
    @commands.command(name="Work", aliases=["work"])
    @cooldown(1,1800,BucketType.member)
    async def work(self, context):
        earn = random.randint(20,30)
        with open("money.json", "r") as f:
            mon = json.load(f)
        mon += earn
        with open("money.json", "w") as f:
            json.dump(mon,f)
        with open("wallet.json", 'r') as f:
            wal = json.load(f)
        wal[str(context.author.id)]["money"] += earn
        with open("wallet.json", 'w') as f:
            json.dump(wal, f, indent=4)
        await context.respond(f"You earned {earn}{coin}!")
    @commands.command(name="Fish", aliases=["fish"])
    @cooldown(1,20,BucketType.member)
    async def fish(self, context):
        itemnum = random.randint(000,999)
        polebreak = random.randint(0,100)
        number = random.randint(0,1000)
        prize = None
        descriptions = {"boot":"just a boot", "goldfish":"A fish of gold","shark":"sharky baby","dildo":"neb's toy when dub isn't around","daddy dubengar":"dadddy dubengar","your father":"your father who went to get the milk the moment you were born"}
        prices = {"boot":20, "goldfish":50,"shark":120,"dildo":300,"daddy dubengar":500,"your father":1000}
        if number <= 1000:
            prize = "nothing"
        if number <= 800:
            prize = "boot"
        if number <= 400:
            prize = "goldfish"
        if number <= 200:
            prize = "shark"
        if number <= 50:
            prize = "dildo"
        if number <= 10:
            prize = "daddy dubengar"
        if number == 1:
            prize = "your father"
        if prize != "nothing" and prize != None:
            item = {
                    "name": prize,
                    "desc": descriptions[prize],
                    "value": prices[prize],
                    "settings": {
                        "addrole": "false",
                        "removerole": "false",
                        "role": "",
                        "sellable": "true"
                    }
                }
            with open("inv.json","r") as f:
                inv = json.load(f)
            if "pole" in inv[str(context.author.id)]:
                if polebreak >= 90:
                    inv[str(context.author.id)].pop("pole")
                    await context.reply("You're pole broke!")
                else:
                    inv[str(context.author.id)][itemnum] = item
                    emb = discord.Embed(title=f"You caught a {prize}!",description=f"You can see it in your inventory. You can use the sell command to sell it for {prices[prize]}{coin}!")
                    await context.reply(embed=emb)
                with open("inv.json","w") as f:
                    json.dump(inv,f,indent=4)
            else:
                await context.reply("You need a fishing pole for this!")

        if prize == "nothing":
            await context.reply(f"You caught nothing :c")
        
    @commands.command(name="Gamble", aliases=["gamble", "Gam", "gam"])
    @cooldown(1,10,BucketType.member)
    async def gamble(self, context, amount):
        amount = int(amount)
        mul = int(random.choice([2,3,4,5]))
        earn = mul*amount
        with open("wallet.json", 'r') as f:
            wall = json.load(f)
        if int(amount) > int(wall[str(context.author.id)]["money"]):
            await context.send("You can not gamble more than you own.")
        if int(amount) <= int(wall[str(context.author.id)]["money"]):
            choices = [":heart:", ":blue_heart:",":orange_heart:"]
            if context.author.id in special:
                chance = random.randint(1,5)
                if chance != 1:
                    earn = amount*10
                    he1 = random.choice(choices)
                    msg = await context.reply(f"{he1}")
                    await asyncio.sleep(2)
                    await msg.edit(content=f"{he1}{he1}")
                    await asyncio.sleep(2)
                    await msg.edit(content=f"{he1}{he1}{he1}")
                    await context.reply(f"You won {earn}{coin}")
                    with open("wallet.json", 'r') as f:
                        wal = json.load(f)
                    wal[str(context.author.id)]["money"] = int(wal[str(context.author.id)]["money"]) + int(earn)
                    with open("wallet.json", 'w') as f:
                        json.dump(wal, f, indent=4)
                    with open("money.json", "r") as f:
                        mon = json.load(f)
                    mon += earn
                    with open("money.json", "w") as f:
                        json.dump(mon,f)
                if chance == 1:
                    mul = int(random.choice([2,3,4,5]))
                    choices = [":heart:", ":blue_heart:",":orange_heart:"]
                    earn = mul*amount
                    he1 = random.choice(choices)
                    he2 = random.choice(choices)
                    he3 = random.choice(choices)
                    if he1 != he2:
                        if he1 != he3:
                            msg = await context.reply(f"{he1}")
                            await asyncio.sleep(2)
                            await msg.edit(content=f"{he1}{he2}")
                            await asyncio.sleep(2)
                            await msg.edit(content=f"{he1}{he2}{he3}")
                            await context.reply(f"You lost {amount}{coin}!")
                            with open("wallet.json", 'r') as f:
                                wal = json.load(f)
                            wal[str(context.author.id)]["money"] = int(wal[str(context.author.id)]["money"]) - int(amount)
                            with open("wallet.json", 'w') as f:
                                json.dump(wal, f, indent=4)
                            with open("money.json", "r") as f:
                                mon = json.load(f)
                            mon -= amount
                            with open("money.json", "w") as f:
                                json.dump(mon,f)
                    if he1 == he2:
                        if he1 == he3:
                            msg = await context.reply(f"{he1}")
                            await asyncio.sleep(2)
                            await msg.edit(content=f"{he1}{he2}")
                            await asyncio.sleep(2)
                            await msg.edit(content=f"{he1}{he2}{he3}")
                            await context.reply(f"You won {earn}{coin}")
                            with open("wallet.json", 'r') as f:
                                wal = json.load(f)
                            wal[str(context.author.id)]["money"] = int(wal[str(context.author.id)]["money"]) + int(earn)
                            with open("wallet.json", 'w') as f:
                                json.dump(wal, f, indent=4)
                            with open("money.json", "r") as f:
                                mon = json.load(f)
                            mon += earn
                            with open("money.json", "w") as f:
                                json.dump(mon,f)
            if not context.author.id in special:
                h1 = ":heart:"
                h2 = ":blue_heart:"
                h3 = ":orange_heart:"
                he1 = random.randint(1,3)
                he2 = random.randint(1,3)
                he3 = random.randint(1,3)
                hea1 = he1
                hea2 = he2
                hea3 = he3
                if not he1 == he2 or not he1 == he3:
                    if he1 == 1:
                        he1 = h1
                    if he1 == 2:
                        he1 = h2
                    if he1 == 3:
                        he1 = h3
                    if he2 == 1:
                        he2 = h1
                    if he2 == 2:
                        he2 = h2
                    if he2 == 3:
                        he2 = h3
                    if he3 == 1:
                        he3 = h1
                    if he3 == 2:
                        he3 = h2
                    if he3 == 3:
                        he3 = h3
                    msg = await context.reply(f"{he1}")
                    await asyncio.sleep(2)
                    await msg.edit(content=f"{he1}{he2}")
                    await asyncio.sleep(2)
                    await msg.edit(content=f"{he1}{he2}{he3}")
                    await context.reply(f"You lost {amount}{coin}!")
                    with open("wallet.json", 'r') as f:
                        wal = json.load(f)
                    wal[str(context.author.id)]["money"] = int(wal[str(context.author.id)]["money"]) - int(amount)
                    with open("wallet.json", 'w') as f:
                        json.dump(wal, f, indent=4)
                    with open("money.json", "r") as f:
                        mon = json.load(f)
                    mon -= amount
                    with open("money.json", "w") as f:
                        json.dump(mon,f)
                he1 = hea1
                he2 = hea2
                he3 = hea3
                if he1 == he2 and he1 == he3:
                    if he1 == 1:
                        he1 = h1
                    if he1 == 2:
                        he1 = h2
                    if he1 == 3:
                        he1 = h3
                    if he2 == 1:
                        he2 = h1
                    if he2 == 2:
                        he2 = h2
                    if he2 == 3:
                        he2 = h3
                    if he3 == 1:
                        he3 = h1
                    if he3 == 2:
                        he3 = h2
                    if he3 == 3:
                        he3 = h3
                    msg = await context.reply(f"{he1}")
                    await asyncio.sleep(2)
                    await msg.edit(content=f"{he1}{he2}")
                    await asyncio.sleep(2)
                    await msg.edit(content=f"{he1}{he2}{he3}")
                    await context.reply(f"You won {earn}{coin}")
                    with open("wallet.json", 'r') as f:
                        wal = json.load(f)
                    wal[str(context.author.id)]["money"] = int(wal[str(context.author.id)]["money"]) + int(earn)
                    with open("wallet.json", 'w') as f:
                        json.dump(wal, f, indent=4)
                    with open("money.json", "r") as f:
                        mon = json.load(f)
                    mon += earn
                    with open("money.json", "w") as f:
                        json.dump(mon,f)
    @commands.command(name="Deposit", aliases=["deposit", "Dep", "dep"])
    async def deposit(self, context, amount):
        with open("bank.json", 'r') as f:
            bank = json.load(f)
        with open("wallet.json", 'r') as f:
            wal = json.load(f)
        otherres = ["All", "all"]
        if not amount in otherres:
            if str(amount) > str(wal[str(context.author.id)]["money"]):
                await context.send(f"You don't have {amount} in your wallet!")
            if str(amount) <= str(wal[str(context.author.id)]["money"]):
                new = int(bank[str(context.author.id)]["money"]) + int(amount)
                wal[str(context.author.id)]["money"] = int(wal[str(context.author.id)]["money"]) - int(amount)
                bank[str(context.author.id)]["money"] = new
                with open("bank.json", "w") as f:
                    json.dump(bank,f,indent=4)
                with open("wallet.json", "w") as f:
                    json.dump(wal,f,indent=4)
                await context.reply(f"You deposited {amount} and your bank's new balance is {new}")
        if amount in otherres:
            bank[str(context.author.id)]["money"] = int(bank[str(context.author.id)]["money"]) + int(wal[str(context.author.id)]["money"])
            wal[str(context.author.id)]["money"] = 0
            newbank = bank[str(context.author.id)]["money"]
            await context.reply(f"Your bank's new balance is {newbank}.")
            with open("bank.json", "w") as f:
                json.dump(bank,f,indent=4)
            with open("wallet.json", "w") as f:
                json.dump(wal,f,indent=4)
    @commands.command(name="Withdraw", aliases=["withdraw", "With", "with"])
    async def withdraw(self, context, amount):
        otherres = ["all", "All"]
        with open("bank.json", 'r') as f:
            bank = json.load(f)
        with open("wallet.json", 'r') as f:
            wal = json.load(f)
        if not amount in otherres:
            if int(amount) > int(bank[str(context.author.id)]["money"]):
                await context.send(f"You don't have {amount} in your bank!")
            if int(amount) < int(bank[str(context.author.id)]["money"]):
                new = int(wal[str(context.author.id)]["money"]) + int(amount)
                wal[str(context.author.id)]["money"] = new
                bank[str(context.author.id)]["money"] = int(bank[str(context.author.id)]["money"]) - int(amount)
                with open("bank.json", "w") as f:
                    json.dump(bank,f,indent=4)
                with open("wallet.json", "w") as f:
                    json.dump(wal,f,indent=4)
                await context.reply(f"You withdrew {amount} and your new balance is {new}")
        if amount in otherres:
            wal[str(context.author.id)]["money"] = int(bank[str(context.author.id)]["money"]) + int(wal[str(context.author.id)]["money"])
            bank[str(context.author.id)]["money"] = 0
            newwal = wal[str(context.author.id)]["money"]
            await context.reply(f"Your new balance is {newwal}.")
            with open("bank.json", "w") as f:
                json.dump(bank,f,indent=4)
            with open("wallet.json", "w") as f:
                json.dump(wal,f,indent=4)
    @commands.command(name="Rob", aliases=["rob"])
    @cooldown(1,10,BucketType.member)
    async def Rob(self, context, member: discord.Member = None):
        with open("wallet.json", "r") as f:
            wal = json.load(f)
        with open("bank.json", "r") as f:
            bank = json.load(f)
        chan = random.randint(1,20)
        fine = random.randint(50,100)
        mon = random.randint(50,100)
        if member == None:
            await context.reply("You can not rob yourself!")
        if not member == None:
            if chan != 1:
                await context.reply(f"You were caught and fined {fine}{coin}!")
                new = int(wal[str(context.author.id)]["money"]) - int(fine)

                if new < 0:
                    bank[str(context.author.id)]["money"] = int(bank[str(context.author.id)]["money"]) + new
                    new = 0
                wal[str(context.author.id)]["money"] = new
                with open("wallet.json", "w") as f:
                    json.dump(wal, f, indent=4)
                with open("bank.json", "w") as f:
                    json.dump(bank, f, indent=4)
                with open("money.json", "r") as f:
                    mon = json.load(f)
                mon -= fine
                with open("money.json", "w") as f:
                    json.dump(mon,f)
            if chan == 1:
                await context.reply(f"You got away! You took {mon}{coin} from {member.display_name}.")
                new = int(wal[str(context.author.id)]["money"]) + int(mon)
                new1 = int(wal[str(member.id)]["money"]) - int(mon)
                if new1 < 0:
                    new1 = 0
                wal[str(context.author.id)]["money"] = new
                wal[str(member.id)]["money"] = new1
                with open("wallet.json", "w") as f:
                    json.dump(wal, f, indent=4)
    @commands.command(name="SetMoney")
    async def setmoney(self, context, member: discord.Member = None, amount = None):
        if context.author.id in owners:
            if amount == None:
                await context.reply("You need to give an amount of money to a user!")
            if member == None:
                member = context.author
            with open("wallet.json", 'r') as f:
                wal = json.load(f)
            with open("money.json", "r") as f:
                mon = json.load(f)
            mon = int(mon) - int(wal[str(member.id)]["money"]) 
            mon = int(mon) + int(amount)
            with open("money.json", "w") as f:
                json.dump(mon,f)
            wal[str(member.id)]["money"] = int(amount)
            with open("wallet.json", 'w') as f:
                json.dump(wal, f, indent=4)
            await context.reply(f"Set {member.display_name}'s money to {amount}.")
        if not context.author.id in owners:
            await context.reply("You do not have permission to use this command!")
    @commands.command(name="Give", aliases=["give"])
    async def give(self, context, member: discord.Member = None, setting = None, amount = None):
        if member == None:
            await context.reply("You need to mention someone to give to!")
        if setting == None:
            if amount == None:
                await context.reply("You need to give this person something!")
            if amount != None:
                with open("wallet.json", 'r') as f:
                    wal = json.load(f)
                if str(amount) > str(wal[str(context.author.id)]["money"]):
                    await context.reply("You don't have enough money to do this!")
                if str(amount) <= str(wal[str(context.author.id)]["money"]):
                    wal[str(member.id)]["money"] = int(wal[str(member.id)]["money"]) + int(amount)
                    wal[str(context.author.id)]["money"] -= amount
                    with open("wallet.json", 'w') as f:
                        json.dump(wal, f, indent=4)
                    await context.reply(f"You gave {amount}{coin} to {member.display_name}.")
        if setting.lower() == "gem":
            if not amount == None:
                nums = ["air","water","fire","earth","ice"]
                if amount in nums:
                    try:
                        role = discord.utils.get(context.guild.roles, name=f"{amount} gem")
                        if not role in context.author.roles:
                            await context.reply("You don't have that role or you need to use it with -use <ID>.")
                        if role in context.author.roles:
                            if role in member.roles:
                                await context.reply(f"{member} already has the {amount} gem")
                            if not role in member.roles:
                                await context.author.remove_roles(role)
                                await member.add_roles(role)
                                await context.reply(f"Successfully gave {member} your {amount} gem")
                    except:
                        await context.send("This is not a valid gem.")
        if setting.lower() == "money":
            if amount == None:
                await context.reply("You need to give this person something!")
            if amount != None:
                with open("wallet.json", 'r') as f:
                    wal = json.load(f)
                if str(amount) > str(wal[str(context.author.id)]["money"]):
                    await context.reply("You don't have enough money to do this!")
                if str(amount) <= str(wal[str(context.author.id)]["money"]):
                    wal[str(member.id)]["money"] = int(wal[str(member.id)]["money"]) + int(amount)
                    wal[str(context.author.id)]["money"] -= int(amount)
                    with open("wallet.json", 'w') as f:
                        json.dump(wal, f, indent=4)
                    await context.send(f"You gave {amount}{coin} to {member.display_name}.")
        if setting.lower() == "item":
            if amount == None:
                await context.send("You need to give this person something!")
            if amount != None:
                with open("inv.json", "r") as f:
                    inv = json.load(f)
                if amount in inv[str(context.author.id)]:
                    item = inv[str(context.author.id)][amount]
                    inv[str(member.id)][amount] = item
                    inv[str(context.author.id)].pop(amount)
                    with open("inv.json", "w") as f:
                        json.dump(inv, f,indent=4)
                    name = item["name"]
                    await context.reply(f"You gave {member.name}, {name}.")
                else:
                    await context.reply("You do not have this item!")
    @commands.command(name="GiveGem", aliases=["givegem"])
    async def givegem(self, context, member:discord.Member, gem):
        if context.author.id in owners:
            gems = {
                "gem1":{
                    "name": "Air_Gem",
                    "desc": "The air gem",
                    "value": 6000.0,
                    "settings": {
                        "addrole": "true",
                        "removerole": "false",
                        "role": "899442749261115392",
                        "sellable": "true"
                    }
                },
                "gem2":{
                    "name": "Water_Gem",
                    "desc": "The water gem",
                    "value": 9000.0,
                    "settings": {
                        "addrole": "true",
                        "removerole": "false",
                        "role": "899449533254230026",
                        "sellable": "true"
                    }
                },
                "gem3":{
                    "name": "Fire_Gem",
                    "desc": "The fire gem",
                    "value": 12000.0,
                    "settings": {
                        "addrole": "true",
                        "removerole": "false",
                        "role": "899449437519224872",
                        "sellable": "true"
                    }
                },
                "gem4":{
                    "name": "Earth_Gem",
                    "desc": "The earth gem",
                    "value": 15000.0,
                    "settings": {
                        "addrole": "true",
                        "removerole": "false",
                        "role": "899449661629268100",
                        "sellable": "true"
                    }
                },
                "gem5":{
                    "name": "Nature_Gem",
                    "desc": "The nature gem",
                    "value": 21000.0,
                    "settings": {
                        "addrole": "true",
                        "removerole": "false",
                        "role": "899452252530548767",
                        "sellable": "true"
                    }
                },
                "gem6":{
                    "name": "Metal_Gem",
                    "desc": "The metal gem",
                    "value": 24000.0,
                    "settings": {
                        "addrole": "true",
                        "removerole": "false",
                        "role": "899452322411868201",
                        "sellable": "true"
                    }
                },
                "gem7":{
                    "name": "Crystal_Gem",
                    "desc": "The crystal gem",
                    "value": 27000.0,
                    "settings": {
                        "addrole": "true",
                        "removerole": "false",
                        "role": "899452393350127716",
                        "sellable": "true"
                    }
                },
                "gem9":{
                    "name": "Dark_Gem",
                    "desc": "The dark gem",
                    "value": 30000.0,
                    "settings": {
                        "addrole": "true",
                        "removerole": "false",
                        "role": "899452510387978291",
                        "sellable": "true"
                    }
                },
                "gem10":{
                    "name": "Light_Gem",
                    "desc": "The light gem",
                    "value": 33000.0,
                    "settings": {
                        "addrole": "true",
                        "removerole": "false",
                        "role": "899452562862927922",
                        "sellable": "true"
                    }
                }
            }
            if gem in gems:
                with open("inv.json","r") as f:
                    inv = json.load(f)
                inv[str(member.id)][gem] = gems[gem]
                with open("inv.json", "w") as f:
                    json.dump(inv,f,indent=4)
                await context.reply(f"Gave {member.mention} the {gem} gem.")
            if not gem in gems:
                await context.reply(f"Gem {gem} is not a gem.")
        if not context.author.id in owners:
            await context.reply("You do not have permission to use this command!")   
    @commands.command(name="AddItem", aliases=["additem"])
    async def additem(self, context, name, *, desc):
        if context.author.id in owners:
            id = random.randint(111,999)
            def check(m):
                return m.author.id == context.author.id
            await context.reply("How much with this it cost?")
            msg = await self.client.wait_for('message', check=check)
            amount = int(msg.content)
            with open("items.json", "r") as f:
                inv = json.load(f)
            inv[str(id)] = {}
            inv[str(id)]["name"] = name
            inv[str(id)]["price"] = amount
            inv[str(id)]["desc"] = desc
            inv[str(id)]["settings"] = {}
            inv[str(id)]["settings"]["addrole"] = "false"
            inv[str(id)]["settings"]["removerole"] = "false"
            inv[str(id)]["settings"]["role"] = ""
            inv[str(id)]["settings"]["sellable"] = "true"
            with open("items.json", "w") as f:
                json.dump(inv,f,indent=4)
            await context.reply(f"Created Item worth {amount} with the name of {name}.")
        if not context.author.id in owners:
            await context.reply("You do not have permission to use this command!")
    @commands.command(name="RemoveItem", aliases=["removeitem"])
    async def removeitem(self, context, message):
        if context.author.id in owners:
            with open("items.json", "r") as f:
                inv = json.load(f)
            if not str(message) in inv:
                await context.reply(f"Item {message} does not exist.")
            if str(message) in inv:
                inv.pop(str(message))
                await context.reply(f"Successfully deleted item {message}.")
                with open("items.json", "w") as f:
                    json.dump(inv,f,indent=4)
        if not context.author.id in owners:
            await context.reply("You do not have permission to use this command!")
    @commands.command(name="Store", aliases=["Shop", "shop", "store", "listitems", "ListItems"])
    async def store(self, context):
        with open("items.json", "r") as f:
            inv = json.load(f)
        emb = discord.Embed(title="Store")
        for item, value in inv.items():
            emb.add_field(name=f"ID: {item} Name: {inv[item]['name']} Price: {inv[item]['price']}", value=str(inv[item]["desc"]),inline=False)
        await context.reply(embed=emb)
    @commands.command(name="EditItem", aliases=["edititem"])
    async def edititem(self, context, id, setting):
        if context.author.id in owners:
            with open("items.json", "r") as f:
                inv = json.load(f)
            if setting == "settings.role":
                def check(m):
                    return m.author.id == context.author.id
                await context.reply(f"What is the role that will be added? (@role)")
                msg1 = await self.client.wait_for('message', check=check)
                role = msg1.content[3:]
                role = role[:-1]
                inv[str(id)]["settings"]["role"] = role
            if setting == "settings.addrole":
                def check(m):
                    return m.author.id == context.author.id
                await context.reply(f"What is the new value for {setting}? (true/false)")
                msg = await self.client.wait_for('message', check=check)
                inv[str(id)]["settings"]["addrole"] = msg.content
                if msg.content == "true":
                    def check(m):
                        return m.author.id == context.author.id
                    await context.reply(f"What is the role that will be added? (@role)")
                    msg1 = await self.client.wait_for('message', check=check)
                    role = msg1.content[3:]
                    role = role[:-1]
                    inv[str(id)]["settings"]["role"] = role
            if setting == "settings.removerole":
                def check(m):
                    return m.author.id == context.author.id
                await context.reply(f"What is the new value for {setting}? (true/false)")
                msg = await self.client.wait_for('message', check=check)
                inv[str(id)]["settings"]["removerole"] = msg.content
                if msg.content == "true":
                    def check(m):
                        return m.author.id == context.author.id
                    await context.reply(f"What is the role that will be added? (@role)")
                    msg1 = await self.client.wait_for('message', check=check)
                    role = msg1.content[3:]
                    role = role[:-1]
                    inv[str(id)]["settings"]["role"] = role
            if setting == "settings.sellable":
                def check(m):
                    return m.author.id == context.author.id
                await context.reply(f"What is the new value for {setting}? (true/false)")
                msg = await self.client.wait_for('message', check=check)
                if msg.content == "true":
                    inv[str(id)]["settings"]["sellable"] = msg.content
                if msg.content == "false":
                    inv[str(id)]["settings"]["sellable"] = msg.content
            if setting == "name":
                def check(m):
                    return m.author.id == context.author.id
                await context.reply(f"What is the new value for {setting}?")
                msg = await self.client.wait_for('message', check=check)
                inv[str(id)]["name"] = msg.content
            if setting == "desc":
                def check(m):
                    return m.author.id == context.author.id
                await context.reply(f"What is the new value for {setting}?")
                msg = await self.client.wait_for('message', check=check)
                inv[str(id)]["desc"] = msg.content
            if setting == "price":
                def check(m):
                    return m.author.id == context.author.id
                await context.reply(f"What is the new value for {setting}?")
                msg = await self.client.wait_for('message', check=check)
                inv[str(id)]["price"] = msg.content
            with open("items.json", "w") as f:
                json.dump(inv,f,indent=4)
        if not context.author.id in owners:
            await context.reply("You do not have permission to use this command!")   
    @commands.command(name="Buy", aliases=["buy"])
    async def buy(self, context, id):
        with open("items.json", "r") as f:
            items = json.load(f)
        with open("inv.json", "r") as f:
            inv = json.load(f)
        with open("wallet.json", "r") as f:
            wal = json.load(f)
        if str(id) in items:
            price = items[str(id)][str("price")]
            with open("money.json", "r") as f:
                mon = json.load(f)
            mon = int(mon) - int(price)
            with open("money.json", "w") as f:
                json.dump(mon,f)
            if int(price) <= int(wal[str(context.author.id)]["money"]):
                wal[str(context.author.id)]["money"] -= int(price)
                await context.reply(f"Successfully bought item {id}.")
                with open("wallet.json", "w") as f:
                    json.dump(wal,f,indent=4)
                inv[str(context.author.id)][id] = {}
                inv[str(context.author.id)][id]["name"] = items[str(id)]["name"]
                inv[str(context.author.id)][id]["desc"] = items[id]["desc"]
                inv[str(context.author.id)][id]["value"] = int(items[str(id)]["price"])*.6
                inv[str(context.author.id)][id]["settings"] = {}
                inv[str(context.author.id)][id]["settings"]["addrole"] = items[id]["settings"]["addrole"]
                inv[str(context.author.id)][id]["settings"]["removerole"] = items[id]["settings"]["removerole"]
                inv[str(context.author.id)][id]["settings"]["role"] = items[id]["settings"]["role"]
                inv[str(context.author.id)][id]["settings"]["sellable"] = items[id]["settings"]["sellable"]

                with open("inv.json", "w") as f:
                    json.dump(inv,f,indent=4)
            else:
                await context.send("You don't have enough money to buy this!")
        if not str(id) in items:
            await context.reply(f"Item {id} does not exist.")
    @commands.command(name="Use", aliases=["use"])
    async def use(self, context, id):
        with open("inv.json", "r") as f:
            inv = json.load(f)
        if str(id) in inv[str(context.author.id)]:
            if inv[str(context.author.id)][id]["settings"]["addrole"] == "true":
                roleid = inv[str(context.author.id)][id]["settings"]["role"]
                role = discord.utils.get(context.guild.roles, id=int(roleid))
                await context.author.add_roles(role)
                await context.reply(f"You successfully used item {inv[str(context.author.id)][id]['name']}")
                inv[str(context.author.id)].pop(id)
                with open("inv.json", "w") as f:
                    json.dump(inv,f,indent=4)
            else:
                await context.reply("You do not have this item!")

    @commands.command(name="Inventory", aliases=["inventory","Inv","inv"])
    async def inventory(self, context, member: discord.Member = None):
        if member == None:
            member = context.author
        with open("inv.json", "r") as f:
            inv = json.load(f)
        if member == None:
            member = context.author
        emb = discord.Embed(title=f"{member.display_name}'s Inventory")
        for item, value in inv[str(member.id)].items():
            emb.add_field(name=f"ID: {item} Name: {inv[str(member.id)][item]['name']} Value: {inv[str(member.id)][item]['value']}", value=str(inv[str(member.id)][item]["desc"]),inline=False)
        await context.reply(embed=emb)
    @commands.command(name="Daily", aliases=["daily", "Day", "day"])
    @cooldown(1,86400,BucketType.member)
    async def daily(self,context):
        with open("wallet.json", 'r') as f:
            wal = json.load(f)
        earn = random.randint(50,100)
        role1 = discord.utils.get(context.guild.roles, id=837687504643293185)
        role2 = discord.utils.get(context.guild.roles, id=837697462256271401)
        role3 = discord.utils.get(context.guild.roles, id=875122021808373790)
        role4 = discord.utils.get(context.guild.roles, id=864347997940744243)
        roles = [role1, role2, role3, role4]
        for role in context.author.roles:
            if role in roles:
                earn = 1000
        wal[str(context.author.id)]["money"] += earn
        with open("wallet.json", 'w') as f:
            json.dump(wal,f,indent=4)
        await context.reply(f"You got a daily amount of {earn}{coin}!")

def setup(client):
    client.add_cog(Economy(client))
