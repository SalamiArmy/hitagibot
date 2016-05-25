# coding=utf-8
import configparser
import urllib
import xml

import telegram
import json
import xml.etree.ElementTree as ET


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


    wikiUrl = 'https://simple.wikiquote.org/w/api.php'
    args = {'action': 'query',
            'list': 'search',
            'srlimit': 1,
            'namespace': 0,
            'format': 'json',
            'srsearch': requestText}
    realUrl = wikiUrl + '?' + urllib.parse.urlencode(args)
    data = json.loads(urllib.request.urlopen(realUrl).read().decode('utf-8'))
    if len(data['query']['search']) >= 1:
        formattedQuoteSnippet = data['query']['search'][0]['snippet'].replace('<span class="searchmatch">', '*').replace(
                '</span>', '*').sub(r'<[^>]*?>', '')
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        return bot.sendMessage(chat_id=chat_id, text=(user + ': ' if not user == '' else '') + formattedQuoteSnippet + \
                                                     '\nhttps://simple.wikiquote.org/wiki/' + \
                                                     urllib.parse.urlencode(data['query']['search'][0]['title']),
                               disable_web_page_preview=True, parse_mode='Markdown')
    else:
        wikiUrl = \
            'https://en.wikiquote.org/w/api.php?action=query&list=search&srlimit=1&namespace=0&format=json&srsearch='
        realUrl = wikiUrl + requestText
        data = json.loads(urllib.request.urlopen(realUrl).read().decode('utf-8'))
        if len(data['query']['search']) >= 1:
            formattedQuoteSnippet = data['query']['search'][0]['snippet']\
                .replace('<span class="searchmatch">', '*')\
                .replace('</span>', '*')\
                .replace('&quot;','\"')
            bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
            return bot.sendMessage(chat_id=chat_id, text=(user + ': ' if not user == '' else '') + formattedQuoteSnippet + \
                                                         '\nhttps://en.wikiquote.org/wiki/' + \
                                                         data['query']['search'][0]['title'].replace(' ', '%20'),
                                   disable_web_page_preview=True, parse_mode='Markdown')

    bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
    return bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                                 ', I\'m afraid I can\'t find any quotes for ' + \
                                                 requestText + '.')

plugin_info = {
    'name': "Quote",
    'desc': "Gets quotes from WikiQuote's API."
}

arguments = {
    'text': [
        "(?i)^[\/](getquote) (.*)"
    ]
}
