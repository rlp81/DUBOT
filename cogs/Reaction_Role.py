import discord
from discord.ext import commands
import json
from discord_components import Button, DiscordComponents
import random

class Reaction_Role(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        DiscordComponents(self.client)
        import aiohttp
        self.session = aiohttp.ClientSession()
    def cog_unload(self):
        self.client.loop.create_task(self.session.close()) 
    @commands.command(name="reaction-role", aliases=["Reaction-Role", "rr", "RR"])
    async def reaction_role(self, ctx, role: discord.Role, emoji, channel: discord.TextChannel):
        ID = random.randint(0000,9999)
        await ctx.send("What message would you like for it to say?")
        def check(m):
            return m.author.id == ctx.author.id
        msg = await self.client.wait_for('message',check=check)
        await channel.send(msg.content, components=[Button(label=f"{emoji} {role}", custom_id=f"{ID}")])
        with open("reaction.json", "r") as f:
            react = json.load(f)
        rr = {
            "roleid": role.id,
            "roleid1": "none"
        }
        react[ID] = {}
        react[ID] = rr
        with open("reaction.json", "w") as f:
            json.dump(react,f,indent=4)
    
    @commands.command(name="reaction-role1", aliases=["Reaction-Role1", "rr1", "RR1"])
    async def reaction_role1(self, ctx, role: discord.Role, role1: discord.Role, emoji, channel: discord.TextChannel):
        ID = random.randint(0000,9999)
        def check(m):
            return m.author.id == ctx.author.id
        msg = await self.client.wait_for('message',check=check)
        await ctx.send("What message would you like for it to say?")
        await ctx.send(msg.content, components=[Button(label=f"{emoji}", custom_id=f"{ID}")])
        with open("reaction.json", "r") as f:
            react = json.load(f)
        rr = {
            "roleid": role.id,
            "roleid1": role1.id
        }
        react[ID] = {}
        react[ID] = rr
        with open("reaction.json", "w") as f:
            json.dump(react,f,indent=4)

    @commands.Cog.listener()
    async def on_button_click(self, interaction):
        ID = interaction.component.custom_id
        with open("reaction.json", "r") as f:
            react = json.load(f)
        rol = react[str(ID)]["roleid"]
        rol1 = react[str(ID)]["roleid1"]
        if not rol1 == "none":
            role1 = discord.utils.get(self.client.get_guild(interaction.guild.id).roles, id=rol1)
        role = discord.utils.get(self.client.get_guild(interaction.guild.id).roles, id=rol)
        member = await interaction.guild.fetch_member(interaction.user.id)
        if not rol1 == "none":
            if role in member.roles:
                await member.remove_roles(role)
                await member.add_roles(role1)
                await interaction.respond(content="Accepted rules")
            if not role in member.roles:
                await member.add_roles(role)
                await member.remove_roles(role1)
                await interaction.respond(content=f"Unaccepted rules")
        if rol1 == "none":
            if role in member.roles:
                await member.remove_roles(role)
                await interaction.respond(content=f"Removed role {role}")
            if not role in member.roles:
                await member.add_roles(role)
                await interaction.respond(content=f"Added role {role}")

def setup(client):
    client.add_cog(Reaction_Role(client))
