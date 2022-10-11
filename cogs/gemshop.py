from datetime import datetime
from threading import Timer
import json
import random
import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

class gemshop(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        self.session = aiohttp.ClientSession()
    def cog_unload(self):
        self.client.loop.create_task(self.session.close()) 
    x=datetime.today()
    y=x.replace(day=x.day+0, hour=0, minute=1, second=0, microsecond=0)
    delta_t=y-x
    secs=delta_t.seconds+1

    def fun():
        with open("items.json", "r") as f:
            items = json.load(f)
        for name, value in items.items():
            if str("gem") in name:
                items.pop(items[name])
        gems = {
            "gem1":{
                "name": "Air_Gem",
                "desc": "The air gem",
                "value": 6000.0,
                "settings": {
                    "addrole": "true",
                    "removerole": "false",
                    "role": "899442749261115392"
                }
            },
            "gem2":{
                "name": "Water_Gem",
                "desc": "The water gem",
                "value": 9000.0,
                "settings": {
                    "addrole": "true",
                    "removerole": "false",
                    "role": "899449533254230026"
                }
            },
            "gem3":{
                "name": "Fire_Gem",
                "desc": "The fire gem",
                "value": 12000.0,
                "settings": {
                    "addrole": "true",
                    "removerole": "false",
                    "role": "899449437519224872"
                }
            },
            "gem4":{
                "name": "Earth_Gem",
                "desc": "The earth gem",
                "value": 15000.0,
                "settings": {
                    "addrole": "true",
                    "removerole": "false",
                    "role": "899449661629268100"
                }
            },
            "gem5":{
                "name": "Nature_Gem",
                "desc": "The nature gem",
                "value": 21000.0,
                "settings": {
                    "addrole": "true",
                    "removerole": "false",
                    "role": "899452252530548767"
                }
            },
        }
        nums = ["gem1","gem2","gem3","gem4","gem5"]
        gem = random.choice(gems)
        for i in nums:
            if i == gem:
                items[i] = gem
        with open("items.json", "w") as f:
            json.dump(items,f,indent=4)
    t = Timer(secs, fun)
    t.start()

def setup(client):
    client.add_cog(gemshop(client))