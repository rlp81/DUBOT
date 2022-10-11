import discord
import json
from discord.ext import commands

class Leaderboard(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    @commands.command(name="Leader",aliases=["Leaderboard","leaderboard","leader"])
    async def leader(self,context):
        with open("levels.json", "r") as f:
            levels: dict = json.load(f)
        exps = {}
        for key, value in levels.items():
            exp = int(levels[key]["exp"])
            exps[int(key)] = exp
        exps = dict(sorted(exps.items(), key=lambda item: item[1],reverse=True))
        num = 0
        finals = {}
        for key,value in exps.items():
            num += 1
            if not num > 10:
                finals[key] = value
        emb = discord.Embed(title="Leaderboard")
        for key, value in finals.items():
            user = self.client.get_user(key)
            level = levels[str(key)]["level"]
            exp = levels[str(key)]["exp"]
            emb.add_field(name=user,value=f"Level: {level}, Exp: {exp}", inline=False)
        await context.reply(embed=emb)
def setup(client):
    client.add_cog(Leaderboard(client))