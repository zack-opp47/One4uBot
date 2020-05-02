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


users = []
with open('kanxck.csv', encoding='UTF-8') as f:
    rows = csv.reader(f,delimiter=",",lineterminator="\n")
    next(rows, None)
    for row in rows:
        user = {}
        user['username'] = row[0]
        user['id'] = int(row[1])
        user['access_hash'] = int(row[2])
        user['name'] = row[3]
        users.append(user)

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

print('\033[1;32mChoose a group to add members:\033[1;33m')
i=0
for group in groups:
    print(str(i) + '- ' + group.title)
    i+=1

g_index = input(" \033[1;34mPileh nomer Add Grup : \033[1;36m")
target_group=groups[int(g_index)]

target_group_entity = InputPeerChannel(target_group.id,target_group.access_hash)

mode = int(('1'))

n = 0

for user in users:
    n += 1
    if n % 50 == 0:
        print(" \033[1;33mAnda Sudah Add 50 User sleep 15 menit\033[1;36m")
        sleep(100)
    try:
        print (" \033[1;36mAdd user \033[1;35m=> \033[1;32m {}".format(user['name']))
        if mode == 1:
            if user['username'] == "":
                continue
            user_to_add = client.get_input_entity(user['username'])
        elif mode == 2:
            user_to_add = InputPeerUser(user['id'], user['access_hash'])
        else:
            sys.exit(" \033[1;31mInvalid Mode Selected. Please Try Again.\033[1;36m")
        client(InviteToChannelRequest(target_group_entity,[user_to_add]))
    except PeerFloodError:
        print(" \033[1;37mGetting Flood Error from telegram. Script is stopping now. Please try again after some time.\033[1;36m")
    except UserPrivacyRestrictedError:
        print(" \033[1;34mThe user's privacy settings do not allow you to do this. Skipping.\033[1;36m")
    except:
        continue
