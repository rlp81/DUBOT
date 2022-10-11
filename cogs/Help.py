import discord
from discord.ext import commands
import os
import random
import aiohttp
class embeds():
    mememb= discord.Embed(title="Help Memes", description=f"Help for memes, Optional() Required<>")
    mememb.add_field(name="RMeme", value="-RMeme (subreddit), sends a random meme from reddit.",inline=False)
    mememb.add_field(name="RMemes", value="-RMemes, lists supported subreddits.",inline=False)
    mememb.add_field(name="Memes", value="-Memes, lists all the memes that can be used by -Meme.", inline=False)
    mememb.add_field(name="Meme", value="-Meme (meme-name), retrieves a meme, if no arguements are given it will get a random meme.", inline=False)
    musemb= discord.Embed(title="Help Music", description=f"Help for music, Optional() Required<>")
    musemb.add_field(name="Join",value="-Join, Joins a voice channel.",inline=False)
    musemb.add_field(name="Leave",value="-Leave, Leaves the voice channel.",inline=False)
    musemb.add_field(name="Play",value="-Play <url/name>, Plays a song",inline=False)
    musemb.add_field(name="Skip",value="-Skip, Skips the currently playing song.",inline=False)
    musemb.add_field(name="Pause",value="-Pause, Pauses currently playing music.",inline=False)
    musemb.add_field(name="Resume",value="-Resume, Resumes paused music,",inline=False)
    musemb.add_field(name="Stop",value="-Stop, Stops all music.",inline=False)
    musemb.add_field(name="Loop",value="-Loop, Loops/unloops the song currently playing.",inline=False)
    musemb.add_field(name="NowPlaying",value="-NowPlaying, Shows the song currently playing",inline=False)
    musemb.add_field(name="Queue",value="-Queue, Lists songs in queue.",inline=False)
    musemb.add_field(name="Remove",value="-Remove <int>, Removes an item from the queue.",inline=False)
    musemb.add_field(name="ClearQueue",value="-ClearQueue, Clears the queue.",inline=False)
    ecoemb= discord.Embed(title="Help Economics", description=f"Help for economics, Optional() Required<>")
    ecoemb.add_field(name="Balance",value="-Balance, (@user), Shows the balances of a user.",inline=False)
    ecoemb.add_field(name="Inventory",value="-Inventory, Shows the inventory of a user.",inline=False)
    ecoemb.add_field(name="Shop",value="-Shop, Show's the server's store of items.",inline=False)
    ecoemb.add_field(name="Gamble",value="-Gamble <number>, Gambling is dangerous you have a 1.3 percent chance of winning and getting the highest multiplier.",inline=False)
    ecoemb.add_field(name="Deposit",value="-Deposit <number>, Deposits an amount of money into your bank.",inline=False)
    ecoemb.add_field(name="Withdraw",value="-Withdraw <number>, Withdraws an amount of money from your bank.",inline=False)
    ecoemb.add_field(name="Give",value="-Give <@user> <amount>, Gives a person your money.",inline=False)
    ecoemb.add_field(name="Rob",value="-Rob <@user>, Your committing an illegal act, what the hell bro.",inline=False)
    ecoemb.add_field(name="AddItem",value="-AddItem <name> <description>, Adds an item to the shop.",inline=False)
    ecoemb.add_field(name="RemoveItem",value="-RemoveItem <id>, Removes an item from the store.",inline=False)
    ecoemb.add_field(name="SetMoney",value="-SetMoney <@user> <amount>, Sets a users wallet to an amount.",inline=False)
    ecoemb.add_field(name="EditItem",value="-EditItem <id> <setting>, Edits an already existing item in the shop.",inline=False)
    ecoemb.add_field(name="Buy",value="-Buy <id>, Buys an item from the shop.",inline=False)
    ecoemb.add_field(name="Use",value="-Use <id>, Uses an item in your inventory.",inline=False)
    ecoemb.add_field(name="Daily",value="-Daily, Gives you yoru daily dose of economics.",inline=False)
    basicemb= discord.Embed(title="Help command", description=f"Help for DUBOT, Optional() Required<>")
    basicemb.add_field(name="Shutdown",value="-Shutdown, Shuts down the bot.",inline=False)
    basicemb.add_field(name="AI", value="-AI <question>, Asks the AI a question.",inline=False)
    basicemb.add_field(name="Ping",value="-Ping, gives you the latency of the bot.",inline=False)
    basicemb.add_field(name="RMeme", value="-RMeme (subreddit), sends a random meme from reddit.",inline=False)
    basicemb.add_field(name="RMemes", value="-RMemes, lists supported subreddits.",inline=False)
    basicemb.add_field(name="Memes", value="-Memes, lists all the memes that can be used by -Meme.", inline=False)
    basicemb.add_field(name="Meme", value="-Meme (meme-name), retrieves a meme, if no arguements are given it will get a random meme.", inline=False)
    basicemb.add_field(name="Mute",value="-Mute @member <reason>, mutes a member.",inline=False)
    basicemb.add_field(name="UnMute",value="-UnMute @member, unmutes a member.",inline=False)
    basicemb.add_field(name="Tier",value="-Tier (@user), Shows tier/level of a user.",inline=False)
    basicemb.add_field(name="Leaderboard",value="-Leaderboard, Shows the level leaderboard.",inline=False)
    basicemb.add_field(name="bonk",value="-bonk (@user), bonk",inline=False)
    basicemb.add_field(name="Giveaway",value="-Giveaway <channel> <message>, bonk",inline=False)
    basicemb.add_field(name="slap",value="-slap (@user), slap slap",inline=False)
    basicemb.add_field(name="wanted",value="-wanted (@user), wild westy testy your wanted",inline=False)
    basicemb.add_field(name="Reaction_Role",value="-Reaction_Role <@role> <Emoji> <message>",inline=False)
    basicemb.add_field(name="Clear",value="-Clear <number>, Clears number of messages",inline=False)
    basicemb.add_field(name="Shutdown",value="-Shutdown, You must be as pog as Coal to use this (you cant).",inline=False)
    basicemb.add_field(name="Economy",value="-Help Economy, Helps you with the bot's economy.",inline=False)
    basicemb.add_field(name="Memes",value="-Help Memes, Helps you with the bot's memes.",inline=False)
    basicemb.add_field(name="Music",value="-Help Music, Helps you with the bot's music system.",inline=False)
class help(commands.Cog):
    
     def __init__(self, client):
          self.client = client
          self.session = aiohttp.ClientSession()
     
     def cog_unload(self):
        self.client.loop.create_task(self.session.close()) 
     @commands.command(name="help", aliases=["Help"])
     async def help(self,context, message = None):
          if message == None:
               await context.reply(embed=embeds.basicemb)
          else:
               if message == "Music":
                    await context.reply(embed=embeds.musemb)
               if message == "Economy":
                    await context.reply(embed=embeds.ecoemb)
               if message == "Memes":
                    await context.reply(embed=embeds.mememb)
            
        

def setup(client):
    client.add_cog(help(client))
