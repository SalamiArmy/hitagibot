import http
import json
import string
import urllib
import random
import configparser
import socket
import telegram as telegram
import logging

import tgapi


def main(tg):
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # Read keys.ini file at program start (don't forget to put your keys in there!)
    keyConfig = configparser.ConfigParser()
    keyConfig.read("keys.ini")
    
    chat_id = tg.message['chat']['id']
    message = tg.message['text']
    user = tg.message['from']['username'] \
        if not tg.message['from']['username'] == '' \
        else tg.message['from']['first_name'] + (' ' + tg.message['from']['last_name']) \
            if not tg.message['from']['last_name'] == '' \
            else ''
            
    message = message.replace(tg.misc['bot_info']['username'], "")

    splitText = message.split(' ', 1)

    requestText = splitText[1] if ' ' in message else ''

    # Ashley: Added a try catch here-
    # For weird 'Unautherized' error when sending photos.
    # Keeps track of the last user to receive a chat action.
    # Satisfies pending chat actions with a message instead of a photo.
    try:
        googurl = 'https://www.googleapis.com/customsearch/v1'
        args = {'cx': keyConfig.get('Google', 'GCSE_SE_ID'),
                'key': keyConfig.get('Google', 'GCSE_APP_ID'),
                'searchType': "image",
                'safe': "off",
                'q': requestText,
                'searchType': "image"}
        realUrl = googurl + '?' + urllib.parse.urlencode(args)
        data = json.loads(urllib.request.urlopen(realUrl).read().decode('utf-8'))
        if 'items' in data and len(data['items']) >= 9:
            imagelink = 'x-raw-image:///'
            offset = 0
            randint = random.randint(0, 9)
            while imagelink.startswith('x-raw-image:///') and \
                            offset < 10 and \
                            randint + offset < len(data['items']):
                imagelink = data['items'][randint + offset]['link']
                offset = offset+1
            if not imagelink.startswith('x-raw-image:///') and not imagelink == '':
                tg.send_message(imagelink)
                #tg.send_photo(imagelink)
            else:
                tg.send_message('I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                ', I\'m afraid I can\'t find any images for ' + \
                                string.capwords(requestText.encode('utf-8')))
        else:
            tg.send_message('I\'m sorry ' + (user if not user == '' else 'Dave') + \
                            ', I\'m afraid I can\'t find any images for ' + \
                            string.capwords(requestText.encode('utf-8')))
    except telegram.TelegramError or \
            socket.timeout or socket.error or \
            urllib.error.URLError or \
            http.client.BadStatusLine as e:
        adminGroupId = keyConfig.get('HeyBoet', 'ADMIN_GROUP_CHAT_ID')
        if user != adminGroupId:
            tg.send_message(requestText + ': ' + imagelink)
        if not adminGroupId == '':
            tg.send_message(
            'Error: ' + e.message + '\n' +
            'Request Text: ' + requestText + '\n' +
            'Url: ' + imagelink)


plugin_info = {
    'name': "Get",
    'desc': "Gets images!"
}

arguments = {
    'text': [
        "^[/](get) (.*)"
    ]
}
