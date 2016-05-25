# coding=utf-8
import configparser
import http
import socket
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
        booksUrl = 'https://www.googleapis.com/books/v1/volumes'
        args = {'key': keyConfig['Google']['GCSE_APP_ID'],
                'q': requestText,
                'maxResults': 1}
        realUrl = booksUrl + '?' + urllib.parse.urlencode(args)
        data = json.loads(urllib.request.urlopen(realUrl).read().decode('utf-8'))
        if 'totalItems' in data and data['totalItems'] >= 1:
            bookData = data['items'][0]['volumeInfo']
            googleBooksUrl = data['items'][0]['accessInfo']['webReaderLink']
            if 'imageLinks' in bookData:
                bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)
                return bot.sendPhoto(chat_id=chat_id, photo=bookData['imageLinks']['thumbnail'],
                                     caption=(user + ': ' if not user == '' else '') + googleBooksUrl)
            else:
                bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
                bot.sendMessage(chat_id=chat_id, text=(user + ': ' if not user == '' else '') + googleBooksUrl)

        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        return bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + user + ', I\'m afraid I can\'t find any books for ' + \
                                                     requestText + '.')
    except telegram.TelegramError or \
            socket.timeout or socket.error or \
            urllib.error.URLError or \
            http.client.BadStatusLine as e:
        adminGroupId = keyConfig['HeyBoet']['ADMIN_GROUP_CHAT_ID']
        if user != adminGroupId:
            return tg.send_message(requestText + ': ' + bookData['imageLinks']['thumbnail'])
        if not adminGroupId == '':
            tg.send_message(
            'Error: ' + e.message + '\n' +
            'Request Text: ' + requestText + '\n' +
            'Url: ' + bookData['imageLinks']['thumbnail'])

plugin_info = {
    'name': "Book",
    'desc': "Gets book information from Google Book's API."
}

arguments = {
    'text': [
        "(?i)^[\/](getbook) (.*)"
    ]
}
