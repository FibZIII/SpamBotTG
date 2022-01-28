from telethon import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

import time
import sqlscripts


from config import (API_ID, API_HASH, SESSION_STRING,chats_to_parsing)



def join_chaneel():

    #Join channels and filter them for actual_channel and dead_channel and save it at db
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


def get_users_from_channels():

    channels = sqlscripts.get_data_to_parsing()
    all_participants = []

    for channel in channels:

        counter = 0
        offset = 0
        limit = 100
        
        channel_object = client.get_entity(channel)

        while True:
            participants = client(GetParticipantsRequest(
                                  channel_object,
                                  ChannelParticipantsSearch(''),
                                  offset,
                                  limit,
                                  hash=0
                                 ))

            if not participants.users:
                break

            for user in participants.users:
                if user.id in all_participants:
                    pass
                else:
                    all_participants.append(user.id)

            offset += len(participants.users)
            counter += len(participants.users)
            time.sleep(10)
            
    return all_participants