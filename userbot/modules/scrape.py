from telethon import TelegramClient, sync, events
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
from colorama import Fore, init as color_ama
import csv
import traceback
from time import sleep
import json,re,sys,os
import getpass
import argparse
import requests
from telethon.errors import SessionPasswordNeededError
from telethon import TelegramClient, sync, events
from telethon.tl.functions.messages import GetHistoryRequest, GetBotCallbackAnswerRequest
from telethon.errors import FloodWaitError

if not os.path.exists("session"):
    os.makedirs("session")
    
os.system("clear")
api_id = 525020
api_hash = '4295ae10915bc5f88786d0bca1839a5d'
nomer = sys.argv[1]
phone = nomer
client = TelegramClient("session/"+phone, api_id, api_hash)
client.connect()
if not client.is_user_authorized():
	try:
		client.send_code_request(phone)
		me = client.sign_in(phone, input(' \033[1;32mEnter the code \033[1;33m '))
	except SessionPasswordNeededError:
			passw = input(" \033[1;36mYour 2fa Password \033[1;34   ")
			me = client.start(phone,passw)
        
os.system("clear")

print('    \033[1;34mTest Drive \033[1;33m=> \033[1;36mKanxck \033[0m\n\n')

chats = []
last_date = None
chunk_size = 200
groups=[]

result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup== True:
            groups.append(chat)
    except:
        continue
print('\033[1;36mmileh grupe scrape members:\033[1;35m')
i=0
for g in groups:
    print(str(i) + '- ' + g.title)
    i+=1

g_index = input(" \033[1;33mPileh nomer scrape user : \033[1;36m")
target_group=groups[int(g_index)]

print('\033[1;31mFetching Members...')
all_participants = []
all_participants = client.get_participants(target_group, aggressive=True)

print('\033[1;37mSaving File In to kanxck.csv')
with open("kanxck.csv","w",encoding='UTF-8') as f:
    writer = csv.writer(f,delimiter=",",lineterminator="\n")
    writer.writerow(['username','user id', 'access hash','name','group', 'group id'])
    for user in all_participants:
        if user.username:
            username= user.username
        else:
            username= ""
        if user.first_name:
            first_name= user.first_name
        else:
            first_name= ""
        if user.last_name:
            last_name= user.last_name
        else:
            last_name= ""
        name= (first_name + ' ' + last_name).strip()
        writer.writerow([username,user.id,user.access_hash,name,target_group.title, target_group.id])      
print('\033[1;36mMembers scraped successfully.')
