import discord
import datetime
import hashlib
from tinydb import TinyDB,Query
from settings import *
from key import TOKEN

db = TinyDB("./db.json")
GIF = Query()

client = discord.Client()

KEYWORDS = [KEYWORDS_KR,KEYWORDS_ENG]
LIST = 'list'
DELETE = 'delete'
REGISTER = 'register'
LOAD = 'load'

def multiple_remove(string,wordlist):
    result = string
    for word in wordlist:
        result = result.replace(word,'')
    return result

@client.event
async def on_ready():
    print(WELCOME)

@client.event
async def on_message(message):
    # image lists
    if any([message.content == x[LIST] for x in KEYWORDS]):
        conlist = db.search(GIF.word != None)
        replmessage = IMAGE_LIST + str([x['word'] for x in conlist]) + HOWTOUSE_LOAD
        await client.send_message(message.channel,replmessage)

    #delete image
    elif any([message.content.startswith(x[DELETE]+' ') for x in KEYWORDS]):
        keyword = multiple_remove(message.content, [x[DELETE]+' ' for x in KEYWORDS])
        matchs = db.search(GIF.word == keyword)
        if matchs:
            db.remove(GIF.word == keyword)
            await client.send_message(message.channel, DELETE_MESSAGE.format(keyword))
        else:
            await client.send_message(message.channel,ERROR_NOTFOUND.format(keyword))
    
    #register new image
    elif any([message.content.startswith(x[REGISTER]+' ') for x in KEYWORDS]):
        keyword = multiple_remove(message.content, [x[REGISTER]+' ' for x in KEYWORDS])
        matchs = db.search(GIF.word == keyword)
        if matchs:
            await client.send_message(message.channel,ERROR_EXIST_ALREADY.format(keyword))
        else:
            try:
                db.insert({
                    'url' : message.attachments[0]["url"],
                    'author' : message.author.name,
                    'word' : keyword
                })
                replmessage = ADDED_NEW_IMAGE.format(message.author.name)
                replmessage += HOWTOUSE_LOAD.format(keyword)
                await client.send_message(message.channel,replmessage)
            except Exception as e:
                print(e)
                await client.send_message(message.channel, ERROR_ADD)

    #load image
    elif any([message.content.startswith(x[LOAD]+' ') for x in KEYWORDS]):
        keyword = multiple_remove(message.content, [x[LOAD]+' ' for x in KEYWORDS])
        matchs = db.search(GIF.word == keyword)
        if matchs:
            await client.send_message(message.channel,matchs[0]['url'])
        else:
            await client.send_message(message.channel,ERROR_NOTFOUND.format(keyword) + '\n'+ HOWTOUSE_REGISTER)

            
client.run(TOKEN)