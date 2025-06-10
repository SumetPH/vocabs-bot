from fastapi import APIRouter
from utils.llm import test_llm
from utils.line import line_random_vocab, line_conversation_sample

router = APIRouter()

@router.get("/api/random-vocab")
async def get_random_vocab():
    try:
        await line_random_vocab(type='push')
        return {"message": "successfully"}
    except:
        return {"message": "error"}

@router.get("/api/conversation-sample")
async def get_conversation_sample():
    try:
        await line_conversation_sample(type='push')
        return {"message": "successfully"}
    except:
        return {"message": "error"}

@router.get('/api/test')
async def test_router():
    result = await test_llm()
    return {"message": result}