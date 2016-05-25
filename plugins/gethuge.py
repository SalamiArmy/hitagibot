# coding=utf-8
import configparser
import string
import urllib

import telegram
import json


def main(tg):
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

    googurl = 'https://www.googleapis.com/customsearch/v1?'
    args = {'cx': keyConfig['Google']['GCSE_SE_ID'],
            'key': keyConfig['Google']['GCSE_APP_ID'],
            'searchType': 'image',
            'safe': 'off',
            'q': requestText,
            'searchType': 'image',
            'num': 10,
            'imgSize': 'huge'}
    realUrl = googurl + urllib.parse.urlencode(args)
    data = json.loads(urllib.request.urlopen(realUrl).read().decode('utf-8'))
    if 'items' in data:
        imagelink = 'x-raw-image:///'
        offset = 0
        while imagelink.startswith('x-raw-image:///') and offset < 10 and offset < len(data['items']):
            imagelink = data['items'][offset]['link']
            offset = offset + 1
        if not imagelink.startswith('x-raw-image:///'):
            bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
            return bot.sendPhoto(chat_id=chat_id, photo=imagelink,
                                 caption=(user + ': ' if not user == '' else '') +
                                         requestText.title() +
                                         (' ' + imagelink if len(imagelink) < 100 else ''))

    bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
    return bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                                 ', I\'m afraid I can\'t find a huge image for ' + \
                                                 string.capwords(requestText) + '.')

plugin_info = {
    'name': "Get Huge Image",
    'desc': "Gets huge images with Google's Custom Search API."
}

arguments = {
    'text': [
        "(?i)^[\/](gethuge) (.*)"
    ]
}
