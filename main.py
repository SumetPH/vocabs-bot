from routers import index, line
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv() 

app = FastAPI()

origins = ["*"]

app.add_middleware(
   CORSMiddleware,
   allow_origins=origins,
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)

app.include_router(index.router)
app.include_router(line.router)

@app.get('/')
async def root():
    return "Vocabs Bot"