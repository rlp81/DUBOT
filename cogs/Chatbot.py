from click import command
import discord
from discord.ext import commands
import random
import json 
import numpy as np
import pickle
from tensorflow import keras
class AIinfo:
    username = "User"
with open("intents.json") as file:
    data = json.load(file)
model = keras.models.load_model('chat_model')
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)
with open('label_encoder.pickle', 'rb') as enc:
    lbl_encoder = pickle.load(enc)
max_len = 20
class Chatbot(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.command(name="setaichannel",aliases=["aichannel"])
    async def setaichannel(self, context, channel: discord.TextChannel = None):
        if context.author.id == 614257135097872410:
            if channel == None:
                channel = context.channel
            with open("info.json","r") as f:
                info = json.load(f)
            info[channel.guild.id] = channel.id
            with open("info.json","w") as f:
                info = json.dump(info,f,indent=4)
            await context.send(f"Set DUBOTAI to {channel}!")
        else:
            await context.reply("You can not run this command.")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        aichannel = None
        with open("info.json","r") as f:
            info = json.load(f)
        if str(message.guild.id) in info:
            aichannel = info[str(message.guild.id)]
            if aichannel == message.channel.id:
                inp = message.content
                result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([inp]),
                                                    truncating='post', maxlen=max_len))
                tag = lbl_encoder.inverse_transform([np.argmax(result)])
                for i in data['intents']:
                    if i['tag'] == tag:
                        respp = random.choice(i['responses'])
                        if i["tag"] == "greeting":
                            if AIinfo.username == None:
                                respp = respp[:-1]
                            else:
                                respp = respp+f" {message.author.display_name}"
                        if message.author.id == self.client.user.id:
                            pass
                        else:
                            await message.channel.send(respp)

            else:
                pass
def setup(client):
    client.add_cog(Chatbot(client))