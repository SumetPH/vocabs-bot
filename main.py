import os
import asyncio
from routers import router_index
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.bot import bot


load_dotenv() 

app = FastAPI()

origins = [
    "http://localhost:3001",
    "https://words-bot-discord-production.up.railway.app"
]

app.add_middleware(
   CORSMiddleware,
   allow_origins=origins,
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)

app.include_router(router_index.router)

@app.get('/')
async def root():
    return "Words Bot Discord"

loop = asyncio.get_event_loop()
loop.create_task(bot.start(os.getenv("DISCORD_BOT_TOKEN")))