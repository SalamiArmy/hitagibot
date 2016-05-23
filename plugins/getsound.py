# coding=utf-8
import configparser
import logging

import soundcloud

import telegram


# reverse image search imports:


def main(tg):
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # Read keys.ini file at program start (don't forget to put your keys in there!)
    keyConfig = configparser.ConfigParser()
    keyConfig.read(["keys.ini", "config.ini", "..\keys.ini", "..\config.ini"])

    chat_id = tg.message['chat']['id']
    message = tg.message['text']
    user = tg.message['from']['username'] \
        if not tg.message['from']['username'] == '' \
        else tg.message['from']['first_name'] + (' ' + tg.message['from']['last_name']) \
        if not tg.message['from']['last_name'] == '' \
        else ''
    botName = tg.misc['bot_info']['username']

    message = message.replace(botName, "")

    splitText = message.split(' ', 1)

    requestText = splitText[1] if ' ' in message else ''

    bot = telegram.Bot(keyConfig['BOT_CONFIG']['token'])

    client = soundcloud.Client(client_id=keyConfig.get('Soundcloud', 'SC_CLIENT_ID'))
    track = client.get('/tracks', q=requestText, sharing='public')
    if len(track) >= 1:
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        userWithCurrentChatAction = chat_id
        urlForCurrentChatAction = (user + ': ' if not user == '' else '') + \
                                  track[0].permalink_url
        bot.sendMessage(chat_id=userWithCurrentChatAction, text=urlForCurrentChatAction)
    else:
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        userWithCurrentChatAction = chat_id
        urlForCurrentChatAction = 'I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                  ', I\'m afraid I can\'t find the sound of ' + \
                                  requestText + '.'
        bot.sendMessage(chat_id=chat_id, text=urlForCurrentChatAction)

plugin_info = {
    'name': "Sound",
    'desc': "Gets sounds from SoundCloud's API."
}

arguments = {
    'text': [
        "^[/](getsound) (.*)"
    ]
}
