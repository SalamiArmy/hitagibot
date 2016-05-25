# coding=utf-8
import configparser
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

    googurl = 'https://www.googleapis.com/customsearch/v1'
    args = {'cx': keyConfig['Google']['GCSE_XSE_ID'],
            'key': keyConfig['Google']['GCSE_APP_ID'],
            'safe': 'off',
            'q': requestText}
    realUrl = googurl + '?' + urllib.parse.urlencode(args)
    data = json.loads(urllib.request.urlopen(realUrl).read().decode('utf-8'))
    if data['searchInformation']['totalResults'] >= '1':
        for item in data['items']:
            xlink = item['link']
            if 'xvideos.com/tags/' not in xlink and \
                'xvideos.com/favorite/' not in xlink and \
                'xvideos.com/?k=' not in xlink and \
                'xvideos.com/tags' not in xlink and \
                'pornhub.com/users/' not in xlink and \
                'pornhub.com/video/search?search=' not in xlink and \
                'xvideos.com/profiles/' not in xlink and \
                'xnxx.com/?' not in xlink and \
                'xnxx.com/tags/' not in xlink and \
                'xhamster.com/stories_search' not in xlink and \
                'redtube.com/pornstar/' not in xlink:
                bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
                return bot.sendMessage(chat_id=chat_id, text=(user + ': ' if not user == '' else '') + xlink)

    return bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +
                                                 ', you\'re just too filthy.')

plugin_info = {
    'name': "Get Porn",
    'desc': "Gets porn with Google's Custom Search API."
}

arguments = {
    'text': [
        "(?i)^[\/](getxxx) (.*)"
    ]
}
