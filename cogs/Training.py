import json
from discord.ext import commands
import discord
import numpy as np
with open('intents.json') as file:
    data = json.load(file)
class Training(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.command(name="Training", aliases=["training"])
    async def training(self, context):
        if context.author.id == 614257135097872410:
            try:
                import tensorflow as tf
                from tensorflow import keras
                from tensorflow.keras.models import Sequential
                from tensorflow.keras.layers import Dense, Embedding, GlobalAveragePooling1D
                from tensorflow.keras.preprocessing.text import Tokenizer
                from tensorflow.keras.preprocessing.sequence import pad_sequences
                from sklearn.preprocessing import LabelEncoder
                import pickle
                training_sentences = []
                training_labels = []
                labels = []
                responses = []
                for intent in data['intents']:
                    for pattern in intent['patterns']:
                        training_sentences.append(pattern)
                        training_labels.append(intent['tag'])
                    responses.append(intent['responses'])
                    
                    if intent['tag'] not in labels:
                        labels.append(intent['tag'])
                num_classes = len(labels)
                lbl_encoder = LabelEncoder()
                lbl_encoder.fit(training_labels)
                training_labels = lbl_encoder.transform(training_labels)
                vocab_size = 1000
                embedding_dim = 16
                max_len = 20
                oov_token = "<OOV>"
                tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_token)
                tokenizer.fit_on_texts(training_sentences)
                word_index = tokenizer.word_index
                sequences = tokenizer.texts_to_sequences(training_sentences)
                padded_sequences = pad_sequences(sequences, truncating='post', maxlen=max_len)
                model = Sequential()
                model.add(Embedding(vocab_size, embedding_dim, input_length=max_len))
                model.add(GlobalAveragePooling1D())
                model.add(Dense(16, activation='relu'))
                model.add(Dense(16, activation='relu'))
                model.add(Dense(num_classes, activation='softmax'))
                model.compile(loss='sparse_categorical_crossentropy', 
                            optimizer='adam', metrics=['accuracy'])
                model.summary()
                epochs = 500
                history = model.fit(padded_sequences, np.array(training_labels), epochs=epochs)
                model.save("chat_model")
                with open('tokenizer.pickle', 'wb') as handle:
                    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
                with open('label_encoder.pickle', 'wb') as ecn_file:
                    pickle.dump(lbl_encoder, ecn_file, protocol=pickle.HIGHEST_PROTOCOL)
                await context.send("AI training complete!")
            except:
                await context.send("An error occured.")
        else:
            await context.send("You can not run this command.")
def setup(client):
    client.add_cog(Training(client))