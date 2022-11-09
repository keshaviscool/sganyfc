#!/usr/bin/env python3
import datetime
#api_id = "19047163"
#api_hash = "862113b02cd33cb03892323ed98fe16b"
api_hash = "a75e80d24e0c2265c1741a76a46c4d83"
api_id = "15129587"
from telethon import TelegramClient, events
import pymongo

# Here you define the target channel that you want to listen to:
user_input_channel = 'https://t.me/SGCustom'

filters = ["TLNFC", "TLFC","TRNFC", "TRFC","WLNFC", "WLFC","WRNFC", "WRFC"]
client = TelegramClient('anyfcV2', api_id, api_hash)

print("client is ready")

mongoDbclient = pymongo.MongoClient("mongodb+srv://admin:heAaEjBCFxwNT334@cluster0.7zkgkmk.mongodb.net/?retryWrites=true&w=majority")
db = mongoDbclient['telegram-automated-website']

# get the collection
keywords = db["keywords"]
filter_keywords = db["filter_keywords"]

def update_filter_keywords():
    filters = list()
    for i in filter_keywords.find():
        filters.append(i['keyword'])
    return filters

# Listen to messages from target channel 
@client.on(events.NewMessage(chats=user_input_channel)) 
async def newMessageListener(event):
    # Get message text 
    newMessage = str(event.message.message).lower().strip()
    newMessageDate = event.message.date
    newMessageDate = newMessageDate + datetime.timedelta(hours=8)
    #filters = update_filter_keywords()
    print(newMessage)
    for i in filters:
        if str(i).lower().strip() == newMessage:
            # get event date time
            if "n" in newMessage:
                color = "green"
            else:
                color = "red"
            keywords.insert_one({"keyword": str(newMessage).strip().upper(), "date": newMessageDate, "color": color})
            # await client.forward_messages(entity='me', messages=event.message) # Forward message to your own account

with client: 
    client.run_until_disconnected() 
