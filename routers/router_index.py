import os
from fastapi import APIRouter
from utils.bot import bot, RandomWordView
from utils.word import random_word
from utils.llm import conversation_sample

router = APIRouter()

@router.get("/api/random-word")
async def get_random_word():
    rw = await random_word()
    channel = bot.get_channel(int(os.getenv("DISCORD_TARGET_CHANNEL_ID")))
    if channel:
        await channel.send(rw['word'], view=RandomWordView(word=rw['word']))
        return {"message": "successfully"}
    else:
        return {"message": "channel not found"}

@router.get("/api/conversation-sample")
async def get_conversation_sample():
    rw = await random_word()
    cs = await conversation_sample(word=rw['word'])
    channel = bot.get_channel(int(os.getenv("DISCORD_TARGET_CHANNEL_ID")))
    if channel:
        await channel.send(f"```{cs}```")
        return {"message": "successfully"}
    else:
        return {"message": "channel not found"}
