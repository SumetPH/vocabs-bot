
from langchain.chat_models import init_chat_model
from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv() 

model = init_chat_model("gpt-4o-mini", model_provider="openai")

class GenerateSentence(BaseModel):
    sentence: str = Field(description="generate a sentence with the given vocab")

async def generate_sentence(vocab: str) -> GenerateSentence:
    structured_llm = model.with_structured_output(GenerateSentence)
    prompt = ChatPromptTemplate([
        (
            "human", 
            "generate a sentence with the given vocab: {vocab}"
        ),
    ])
    chain = prompt | structured_llm
    return await chain.ainvoke({"vocab": vocab})

async def translate_vocab(vocab: str) -> str:
    result = model.invoke(f"""
        แปล vocab ที่ให้เป็นภาษาไทย พร้อม คำอ่าน และ parts of speech เช่น

        help (เฮลพฺ) v. ช่วยเหลือ

        vocab : {vocab}
    """)
    return result.content

async def conversation_sample(vocab: str) -> str:
    result = model.invoke(f"""
        สร้าง 1 ประโยคสนทนา พร้อมความหมายบางคำ ด้วย vocab ที่ให้ ตัวอย่างคำตอบ เช่น
                          
        A: Could you help me with this report?
        B: Sure. What do you need help with?

        - help (เฮลพฺ) v. ช่วยเหลือ
        - report (รีพอร์ท) n. รายงาน
        - need (นีด) v. ต้องการ

        vocab: {vocab}
    """)
    return result.content

async def test_llm():
    vocab = "want"
    result = model.invoke(f"""
        แปล vocab ที่ให้เป็นภาษาไทย พร้อม คำอ่าน และ parts of speech เช่น

        help (เฮลพฺ) v. ช่วยเหลือ

        vocab : {vocab}
    """)
    return result.content