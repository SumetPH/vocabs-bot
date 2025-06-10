import os
import httpx
from dotenv import load_dotenv
from utils.vocab import random_vocab, remember_vocab
from utils.llm import generate_sentence, translate_vocab, conversation_sample

load_dotenv()

async def loading():
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
    }
    data = {
        "chatId": os.getenv("LINE_USER_ID")
    }
    async with httpx.AsyncClient() as client:
        response = await client.post("https://api.line.me/v2/bot/chat/loading/start", headers=headers, json=data)
        if response.status_code != 200:
            print(response.json())
        return response.json()

async def push_message(message):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
    }
    data = {
        "to": os.getenv("LINE_USER_ID"),
        "messages": [
            message
        ]
    }
    async with httpx.AsyncClient() as client:
        response = await client.post("https://api.line.me/v2/bot/message/push", headers=headers, json=data)
        if response.status_code != 200:
            print(response.json())
        return response.json()

async def reply_message(reply_token, message):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
    }
    data = {
        "replyToken": reply_token,
        "messages": [
            message
        ]
    }
    async with httpx.AsyncClient() as client:
        response = await client.post("https://api.line.me/v2/bot/message/reply", headers=headers, json=data)
        if response.status_code != 200:
            print(response.json())
        return response.json()


async def line_random_vocab(type, reply_token=None):
    rv = await random_vocab()
    vocab = rv['vocab']
    message = {
        "type": "flex",
        "altText": vocab,
        "contents": {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "Random Vocab",
                        "color": "#ffffff",
                        "weight": "bold"
                    }
                ],
                "backgroundColor": "#3C3D37"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": vocab,
                        "align": "center",
                        "size": "18px"
                    }
                ],
                "paddingTop": "32px",
                "paddingBottom": "32px"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "action": {
                            "type": "message",
                            "label": "Hint",
                            "text": f"#hint {vocab}"
                        },
                        "height": "sm",
                        "style": "primary",
                        "color": "#3C3D37"
                    },
                    {
                        "type": "button",
                        "height": "sm",
                        "action": {
                            "type": "message",
                            "label": "Translate",
                            "text": f"#translate {vocab}"
                        },
                        "style": "primary",
                        "color": "#3C3D37"
                    },
                    {
                        "type": "button",
                        "height": "sm",
                        "action": {
                            "type": "message",
                            "label": "Remember",
                            "text": f"#remember {vocab}"
                        },
                        "style": "primary",
                        "color": "#3C3D37"
                    }
                ],
                "flex": 0
            }
        }
    }

    if(type == 'push'):
        await push_message(message)
    
    if(type == 'reply'):
        await reply_message(reply_token=reply_token, message=message)

async def line_conversation_sample(type, reply_token=None):
    vocab = await random_vocab()
    cs = await conversation_sample(vocab)
    message = {
        "type": "text",
        "text": cs
    }
    
    if type == 'push':
        await push_message(message)
    if type == 'reply':
        await reply_message(reply_token=reply_token, message=message)

async def line_hint_vocab(reply_token, vocab):
    sentence = await generate_sentence(vocab)
    message = {
        "type": "text",
        "text": sentence
    }
    await reply_message(reply_token=reply_token, message=message)

async def line_translate_vocab(reply_token, vocab):
    translate = await translate_vocab(vocab)
    message = {
        "type": "text",
        "text": translate
    }
    await reply_message(reply_token=reply_token, message=message)

async def line_remember_vocab(reply_token, vocab):
    try:
        await remember_vocab(vocab)
        await remember_vocab(vocab)
        message = {
            "type": "text",
            "text": 'Remembered'
        }
        await reply_message(reply_token=reply_token, message=message)
    except:
        message = {
            "type": "text",
            "text": "Error"
        }
        await reply_message(reply_token=reply_token, message=message)
    