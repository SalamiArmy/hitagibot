# coding=utf-8
import configparser
import random

import feedparser

import telegram


def main(tg):
    # Read keys.ini file at program start (don't forget to put your keys in there!)
    keyConfig = configparser.ConfigParser()
    keyConfig.read(["keys.ini", "config.ini", "..\keys.ini", "..\config.ini"])

    chat_id = tg.message['chat']['id']
    user = tg.message['from']['username'] \
        if not tg.message['from']['username'] == '' \
        else tg.message['from']['first_name'] + (' ' + tg.message['from']['last_name']) \
        if not tg.message['from']['last_name'] == '' \
        else ''

    bot = telegram.Bot(keyConfig['BOT_CONFIG']['token'])

    realUrl = 'http://isis.liveuamap.com/rss'
    data = feedparser.parse(realUrl)
    if len(data.entries) >= 1:
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        return bot.sendMessage(chat_id=chat_id, text=(user + ': ' if not user == '' else '') + \
                                                     data.entries[random.randint(0, 9)].link)

    bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
    return bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                                 ', I\'m afraid I can\'t find any ISIS news.')

plugin_info = {
    'name': "ISIS",
    'desc': "Gets a random news article from an isis news rss feed."
}

arguments = {
    'text': [
        "(?i)^[\/](isis)(.*)"
    ]
}
