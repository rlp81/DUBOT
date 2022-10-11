from re import sub
import discord
import asyncpraw
import random
from discord.ext import commands
import json
icon = "https://cdn.discordapp.com/attachments/898697869941428319/912823807130107914/test.png"
async def get_meme(subs):
    reddit = asyncpraw.Reddit(client_id='id',
                        client_secret='secret',
                        user_agent='user')
    choice = random.choice(list(subs))
    memes_submissions = []
    subreddit = await reddit.subreddit(choice)
    async for submission in subreddit.hot(limit=100):
        memes_submissions.append(submission)
    submission = random.choice(memes_submissions)
    #for i in range(0, post_to_pick):
    #submission = random.choice(memes_submissions)next(x for x in memes_submissions if not x.stickied)
    return submission, choice

async def get_meme1(message):
    reddit = asyncpraw.Reddit(client_id='LM8_2efNkuj8E0_qKkxy9g',
                        client_secret='RIGF6cAm4WvtXJD8hlgIDDZmmzTA8w',
                        user_agent='rlp81')
    memes_submissions = []
    subreddit = await reddit.subreddit(f"{message}")
    async for submission in subreddit.hot(limit=100):
        memes_submissions.append(submission)
    submission = random.choice(memes_submissions)
    return submission

class Reddit_Meme(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        import aiohttp
        self.session = aiohttp.ClientSession()
    def cog_unload(self):
        self.client.loop.create_task(self.session.close()) 
    @commands.command(name="Reddit_Meme", aliases=["reddit_meme","RMeme","rmeme","RM","rm"])
    async def reddit_meme(self, context, message = None):
        bans = [818939178661838868]
        if not context.author.id in bans:
            with open("subs.json","r") as f:
                subs = json.load(f)
            sublist = ""
            for sub in subs:    
                sublist += f" {sub}"
            if message == None:
                    async with context.typing():
                        #try:
                        submission, choice = await get_meme(subs)
                        if submission.over_18 == True:
                            await context.send("Did not send meme because it was 18+")
                        if submission.over_18 == False:
                            emb = discord.Embed(title=f"r/{choice}|{submission.title}",description=f"posted by {submission.author}", color=0xff571e)
                            emb.set_image(url=submission.url)
                            emb.set_footer(text="DUBOT Reddit API",icon_url=icon)
                            await context.reply(embed=emb)

                        #except:
                            #await context.send("Failed to send meme")
            if message != None:
                if str(message) in sublist:
                    async with context.typing():
                        try:
                            submission = await get_meme1(message)
                            if submission.over_18 == True:
                                await context.send("Did not send meme because it was 18+")
                            if submission.over_18 == False:
                                emb = discord.Embed(title=f"r/{message}|{submission.title}",description=f"posted by {submission.author}", color=0xff571e)
                                emb.set_image(url=submission.url)
                                emb.set_footer(text="DUBOT Reddit API",icon_url=icon)
                                await context.reply(embed=emb)
                        except:
                            await context.send("Failed to send meme")
                else:
                    await context.send(f"{message} is not a supported subreddit.")
    @commands.command(name="Reddit_Memes", aliases=["reddit_memes","RMemes","rmemes","RMs","rms"])
    async def reddit_memes(self, context):
        bans = [818939178661838868]
        if not context.author.id in bans:
            with open("subs.json","r") as f:
                subs = json.load(f)
            sublist = ""
            for sub in subs:
                sublist += f" {sub}"
            await context.send(f"Supported subreddits:{sublist}")
    

def setup(client):
    client.add_cog(Reddit_Meme(client))
