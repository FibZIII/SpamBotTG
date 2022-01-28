from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon import functions, types
from telethon import events
from telethon.errors import FloodWaitError, UserBannedInChannelError, UsernameInvalidError, ChatAdminRequiredError, ChatWriteForbiddenError
import schedule
import threading
import time
import random
import sqlscripts

from config import (API_ID, API_HASH, SESSION_STRING)



client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

def send_messages():

    #Get text for messages
    f = open('messages.txt', 'r', encoding = 'utf-8')
    list_of_message = [line.strip() for line in f]
    f.close()

    chats_for_messaging = sqlscripts.get_actual_data(status = True, messaging = True)

    for chats in chats_for_messaging:
        
        #Get number message to spam and random choice it
        numb_messege = random.randint(0,99)
        message = list_of_message[numb_messege]
        time.sleep(70)

        #Send messeges for channels
        try:
            client.send_message(chats, message)
            print('Сообщение отправлено:{}\nСообщение: {}'.format(channel, message))

        except UsernameInvalidError as e:
            pass

        except ChatAdminRequiredError as e:
            pass

        except ChatWriteForbiddenError as e:
            pass

        except UserBannedInChannelError as e:
            pass

        except FloodWaitError as e:
            print('Flood waited for', e.seconds)
            time.sleep(e.seconds + 10)
            print('Продолжаю работу')

def join_chaneel():

    #Join channels and filter them for actual_channel and dead_channel and save it at db
    channels = get_data_for_joining()
    for channel_cod in channels:
        print(channel_cod)
        time.sleep(120)

        try:
            client(functions.channels.JoinChannelRequest(channel=channel_cod))
            data = client.get_entity(channel_cod)
            print('actual_channel:{}'.format(channel_cod))
            sqlscripts.add_data_to_channels(channel_id = data.id,
                                            name = data.title,
                                            channel_link = channel_cod,
                                            status = True,
                                            channel_access_hash = data.access_hash,
                                            messaging = True
                                            )

        except ValueError:
            sqlscripts.add_data_to_channels(channel_id = None,
                                            name = 'dead',
                                            channel_link = channel_cod,
                                            status = False,
                                            channel_access_hash = None,
                                            messaging = False
                                            )
            print('dead_channel:{}'.format(channel_cod))

        except UsernameInvalidError as e:
            sqlscripts.add_data_to_channels(channel_id = None,
                                            name = 'dead',
                                            channel_link = channel_cod,
                                            status = False,
                                            channel_access_hash = None,
                                            messaging = False
                                            )
            print('Неправильный юзер: {}'.format(channel_cod))
            pass
        
        except FloodWaitError as e:
            print('Flood waited for', e.seconds)
            time.sleep(e.seconds)
            print('Продолжаю работу')

def get_data_for_joining():

    #Get data from DataBase for filter channels
    actual_channels = sqlscripts.get_data_to_parsing()
    dead_channels = dead_channels = sqlscripts.get_actual_data(status = False, messaging = False)

    #Get data from channels.txt
    f = open('channels.txt', 'r', encoding = 'utf-8')
    channels = [line.strip() for line in f]
    f.close()

    #Filter channels
    for actual_channel in actual_channels:
        try:
            channels.remove(actual_channel)

        except ValueError:
            pass

    for dead_channel in dead_channels:
        try:
            channels.remove(dead_channel)

        except ValueError:
            pass

    #Save changes
    f = open('channels.txt', 'w', encoding = 'utf-8')
    for channel in channels:
        f.write(channel + '\n')
    f.close

    return channels


def runSchedulers():
  
    schedule.every(1).minutes.do(send_messages)

    while True:
        schedule.run_pending()
        time.sleep(1)
        
#RunBot
if __name__ == "__main__":
    sqlscripts.check_db()
    client.start()
    join_chaneel()
    runSchedulers()
    client.run_until_disconnected()