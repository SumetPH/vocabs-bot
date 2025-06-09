import os
from fastapi import APIRouter
from utils.bot import bot, RandomVocabView
from utils.vocab import random_vocab
from utils.llm import conversation_sample

router = APIRouter()

@router.get("/api/random-vocab")
async def get_random_vocab():
    rw = await random_vocab()
    channel = bot.get_channel(int(os.getenv("DISCORD_TARGET_CHANNEL_ID")))
    if channel:
        await channel.send(rw['vocab'], view=RandomVocabView(vocab=rw['vocab']))
        return {"message": "successfully"}
    else:
        return {"message": "channel not found"}

@router.get("/api/conversation-sample")
async def get_conversation_sample():
    rw = await random_vocab()
    cs = await conversation_sample(vocab=rw['vocab'])
    channel = bot.get_channel(int(os.getenv("DISCORD_TARGET_CHANNEL_ID")))
    if channel:
        await channel.send(f"```{cs}```")
        return {"message": "successfully"}
    else:
        return {"message": "channel not found"}
