import os
import asyncio
from dotenv import load_dotenv
from fastapi import FastAPI
from utils.bot import bot, RandomWordView
from utils.word import random_word
# from utils.llm import translate_word

load_dotenv() 

app = FastAPI()

@app.get("/api/random-word")
async def send_message():
    rw = await random_word()
    channel = bot.get_channel(int(os.getenv("DISCORD_TARGET_CHANNEL_ID")))
    if channel:
        await channel.send(rw['word'], view=RandomWordView(word=rw['word']))
        return {"message": "successfully"}

loop = asyncio.get_event_loop()
loop.create_task(bot.start(os.getenv("DISCORD_BOT_TOKEN")))