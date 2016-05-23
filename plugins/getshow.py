# coding=utf-8
import configparser
import logging
import urllib

from html.parser import HTMLParser

import telegram
# reverse image search imports:
import json


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

    showsUrl = 'http://api.tvmaze.com/search/shows?q='
    data = json.loads(urllib.request.urlopen(showsUrl + requestText).read().decode('utf-8'))
    if len(data) >= 1:
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
        userWithCurrentChatAction = chat_id
        urlForCurrentChatAction = data[0]['show']['image']['original']
        bot.sendPhoto(chat_id=chat_id,
                      photo=urlForCurrentChatAction,
                      caption=HTMLParser.strip_tags(data[0]['show']['summary'].replace('\\', '')[:125]))
    else:
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        userWithCurrentChatAction = chat_id
        urlForCurrentChatAction = 'I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                  ', I\'m afraid I cannot find the TV show ' + \
                                  requestText.title()
        bot.sendMessage(chat_id=chat_id, text=urlForCurrentChatAction)

plugin_info = {
    'name': "TV Show",
    'desc': "Gets info about a TV show from TVAmaze's API."
}

arguments = {
    'text': [
        "^[/](getshow) (.*)"
    ]
}
