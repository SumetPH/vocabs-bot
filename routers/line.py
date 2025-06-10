from fastapi import APIRouter
from utils.line import loading, line_random_vocab, line_hint_vocab, line_translate_vocab, line_remember_vocab, line_conversation_sample

router = APIRouter()

@router.post('/line/webhook')
async def line_webhook(data: dict):
    event = data['events'][0]
    reply_token = event['replyToken']

    await loading()

    if event['type'] == 'message':
        text = event['message']['text'].strip().split()

        if text[0] == '#rv':
            text = event['message']['text']
            await line_random_vocab(type='reply', reply_token=reply_token)

        if text[0] == '#cs':
            await line_conversation_sample(type='reply', reply_token=reply_token)
        
        if text[0] == '#hint':
            await line_hint_vocab(reply_token=reply_token, vocab=text[1])

        if text[0] == '#translate':
            await line_translate_vocab(reply_token=reply_token, vocab=text[1])

        if text[0] == '#remember':
            await line_remember_vocab(reply_token=reply_token, vocab=text[1])

    return 'OK'