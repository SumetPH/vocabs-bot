
from langchain.chat_models import init_chat_model
from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv() 

model = init_chat_model("gpt-4o-mini", model_provider="openai")

class GenerateSentence(BaseModel):
    sentence: str = Field(description="generate a sentence with the given word")

async def generate_sentence(word: str) -> GenerateSentence:
    structured_llm = model.with_structured_output(GenerateSentence)
    prompt = ChatPromptTemplate([
        (
            "human", 
            "generate a sentence with the given word: {word}"
        ),
    ])
    chain = prompt | structured_llm
    return await chain.ainvoke({"word": word})

class TranslateTH(BaseModel):
    translate_th: str = Field(description="translate the given word to thai language")
    parts: str = Field(description="parts of speech in english")

async def translate_word(word: str) -> TranslateTH:
    structured_llm = model.with_structured_output(TranslateTH)
    prompt = ChatPromptTemplate([
        (
            "human", 
            "translate the given word to thai language: {word}"
        ),
    ])
    chain = prompt | structured_llm
    return await chain.ainvoke({"word": word})

async def conversation_sample() -> str:
    result = model.invoke("""
        สร้าง 1 ประโยคสนทนา พร้อมความหมายบางคำ ตัวอย่างคำตอบ เช่น
                          
        A: Could you help me with this report?
        B: Sure. What do you need help with?

        - help (v.) ช่วยเหลือ
        - report (n.) รายงาน
        - need (v.) ต้องการ
    """)
    return result.content