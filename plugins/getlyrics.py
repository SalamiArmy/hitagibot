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

    trackUrl = 'http://api.musixmatch.com/ws/1.1/track.search?apikey='
    data = json.loads(urllib.request.urlopen(trackUrl + keyConfig.get('MusixMatch', 'APP_ID') + '&q=' + requestText).read().decode('utf-8'))
    if 'message' in data and \
                    'body' in data['message'] and \
                    'track_list' in data['message']['body'] and \
                    len(data['message']['body']['track_list']) >= 1 and \
                    'track' in data['message']['body']['track_list'][0] and \
                    'artist_name' in data['message']['body']['track_list'][0]['track'] and \
                    'track_name' in data['message']['body']['track_list'][0]['track']:
        artist_name = data['message']['body']['track_list'][0]['track']['artist_name']
        track_name = data['message']['body']['track_list'][0]['track']['track_name']
        track_soundcloud_id = str(data['message']['body']['track_list'][0]['track']['track_soundcloud_id'])
        trackId = str(data['message']['body']['track_list'][0]['track']['track_id'])
        lyricsUrl = 'http://api.musixmatch.com/ws/1.1/track.lyrics.get?apikey='
        data = json.loads(urllib.request.urlopen(lyricsUrl + keyConfig.get('MusixMatch', 'APP_ID') + '&track_id=' + trackId).read().decode('utf-8'))
        lyrics_body = ''
        if 'message' in data and \
                        'body' in data['message'] and \
                        'lyrics' in data['message']['body'] and \
                        len(data['message']['body']['lyrics']) >= 1 and \
                        'lyrics_body' in data['message']['body']['lyrics']:
            lyrics_body = data['message']['body']['lyrics']['lyrics_body'].replace(
                '******* This Lyrics is NOT for Commercial use *******', '')
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        return bot.sendMessage(chat_id=chat_id, text=((user + ': ') if not user == '' else '') + track_name + ' by ' + artist_name + \
                                                     (('\nListen at: https://api.soundcloud.com/tracks/' + track_soundcloud_id) if not track_soundcloud_id == '0' else '') + \
                                                     (('\n' + lyrics_body) if not lyrics_body == '' else ''))

    bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
    return bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') + \
                                                 ', I\'m afraid I can\'t find any tracks for the lyrics ' + \
                                                 requestText)

plugin_info = {
    'name': "Lyrics",
    'desc': "Gets lyrics from Musix Match's API."
}

arguments = {
    'text': [
        "(?i)^[\/](getlyrics) (.*)"
    ]
}
