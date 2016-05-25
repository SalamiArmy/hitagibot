import configparser
import http
import json
import random
import socket
import urllib

import telegram


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
        else 'Dave'
    botName = tg.misc['bot_info']['username']

    message = message.replace(botName, "")

    splitText = message.split(' ', 1)

    requestText = splitText[1] if ' ' in message else ''

    bot = telegram.Bot(keyConfig['BOT_CONFIG']['token'])


    # Ashley: Added a try catch here-
    # For weird 'Unautherized' error when sending photos.
    # Keeps track of the last user to receive a chat action.
    # Satisfies pending chat actions with a message instead of a photo.
    try:
        realUrl = 'https://www.googleapis.com/customsearch/v1?&searchType=image&num=10&safe=off&' \
                  'cx=' + keyConfig.get('Google', 'GCSE_SE_ID') + '&key=' + \
                  keyConfig.get('Google', 'GCSE_APP_ID') + '&q=fig'
        args = {'key': keyConfig['Google']['GCSE_APP_ID'],
                'q': requestText,
                'maxResults': 1}
        data = json.loads(urllib.request.urlopen(realUrl).read().decode('utf-8'))
        if data['searchInformation']['totalResults'] >= 1:
            imagelink = data['items'][random.randint(0, 9)]['link']
            bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
            urlForCurrentChatAction = imagelink.encode('utf-8')
            return bot.sendPhoto(chat_id=chat_id, photo=urlForCurrentChatAction,
                                 caption=user + ': ' + imagelink if len(imagelink) < 100 else '')
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        return bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + user + ', I\'m afraid I can\'t find any figs.')
    except telegram.TelegramError or \
            socket.timeout or socket.error or \
            urllib.error.URLError or \
            http.client.BadStatusLine as e:
        adminGroupId = keyConfig['HeyBoet']['ADMIN_GROUP_CHAT_ID']
        if user != adminGroupId:
            return tg.send_message(requestText + ': ' + imagelink)
        if not adminGroupId == '':
            tg.send_message(
            'Error: ' + e.message + '\n' +
            'Request Text: ' + requestText + '\n' +
            'Url: ' + imagelink)

plugin_info = {
    'name': "Fig",
    'desc': "Gets a fig from Google's Custom Search API."
}

arguments = {
    'text': [
        "(?i)^[\/](getfig)(.*)"
    ]
}
