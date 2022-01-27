from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon import functions, types
from telethon import events
from telethon.errors import FloodWaitError, UsernameInvalidError, ChatAdminRequiredError, ChatWriteForbiddenError, ChannelPrivateError
import schedule
import threading
import time
import random
import sqlscripts

from config import (API_ID, API_HASH, SESSION_STRING,ADMIN, free_agent)



client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)


def send_messages():

    #Get text for messages
    f = open('messages.txt', 'r', encoding = 'utf-8')
    list_of_message = [line.strip() for line in f]
    f.close()

    for channel in actual_channels:
        #Get message to spam and random choice it
        numb_messege = random.randint(0,99)
        message = list_of_message[numb_messege]
        time.sleep(90)

        #Send messeges for channels
        try:
            client.send_message(channel, message)
            print('Сообщение отправлено:{}'.format(channel))

        except FloodWaitError as e:
            print('Flood waited for', e.seconds)
            time.sleep(e.seconds)

        except UsernameInvalidError as e:
            pass

        except ChatAdminRequiredError as e:
            pass

        except ChatWriteForbiddenError as e:
            pass

        except ChannelPrivateError as e:
            pass

def join_chaneel():

    #Join channels and filter them for actual_channel and dead_channel and save it at db
    for channel_cod in channels:
        print(channel_cod)
        time.sleep(120)

        try:
            client(functions.channels.JoinChannelRequest(channel=channel_cod))
            print('actual_channel:{}'.format(channel_cod))
            sqlscripts.add_data_to_channels(channel = channel_cod, status = True)

        except ValueError:
            sqlscripts.add_data_to_channels(channel = channel_cod, status = False)
            print('dead_channel:{}'.format(channel_cod))

        except UsernameInvalidError as e:
            sqlscripts.add_data_to_channels(channel = channel_cod, status = False)
            print('Неправильный юзер: {}'.format(channel_cod))
            pass

        except ChannelPrivateError as e:
            sqlscripts.add_data_to_channels(channel = channel_cod, status = False)
            print('Нет доступа к этой группе: {}'.format(channel_cod))
            pass

        except FloodWaitError as e:
            print('Flood waited for', e.seconds)
            time.sleep(e.seconds)

def get_data_form_txt():

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
    #Create schedule
    schedule.every(2).hours.do(send_messages)
    
    #Loop schedule 
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    sqlscripts.check_db()
    actual_channels = sqlscripts.get_actual_channels()
    dead_channels = sqlscripts.get_dead_channels()
    channels = get_data_form_txt()
    print(actual_channels)
    print(dead_channels)
    print(channels)
    client.start()
    join_chaneel()
    actual_channels = sqlscripts.get_actual_channels()
    dead_channels = sqlscripts.get_dead_channels()
    runSchedulers()
    client.run_until_disconnected()