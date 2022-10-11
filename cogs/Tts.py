import discord
from mutagen.mp3 import MP3
from discord.ext import commands
from discord.ext.commands import has_permissions
import os
import aiohttp
import asyncio
from discord import FFmpegPCMAudio
import gtts
class Tts(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        self.session = aiohttp.ClientSession()
    def cog_unload(self):
        self.client.loop.create_task(self.session.close()) 
    @commands.command(name="Tts", aliases=["TTS", "tts"])
    async def tts(self,context,*,message):
        member_voice = context.author.voice
        self.client_voice = None
        if member_voice and member_voice.channel:
            if context.voice_client:
                await context.send("Bot already in a voice channel!")
            else:
                try:
                    await member_voice.channel.connect()
                    self.client_voice = context.voice_client
                except:
                    await context.send("An error occured make sure you're in a voice channel!")
        else:
            await context.send("You must be in a channel!")
        tts = gtts.gTTS(message)
        tts.save("voice.mp3")
        client_voice = self.client_voice
        audio = MP3("voice.mp3")
        client_voice.play(FFmpegPCMAudio("voice.mp3",executable=r"C:\Users\colel\Desktop\DiscordBots\MattBot\ffmpeg\bin\ffmpeg.exe"))
        await asyncio.sleep(int(audio.info.length)+3)
        os.remove("voice.mp3")
        client_voice.stop()
        await client_voice.disconnect()
        
    
    @tts.error
    async def tts_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You forgot to give input!")
def setup(client):
    client.add_cog(Tts(client))