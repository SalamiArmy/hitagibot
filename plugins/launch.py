# coding=utf-8
import configparser
import datetime
import urllib

from dateutil import tz

import telegram
import json


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

    rocketUrl = urllib.request.Request('https://launchlibrary.net/1.1/launch/next/5', headers={'User-Agent': "Magic Browser"})
    rocketData = json.loads(urllib.request.urlopen(rocketUrl).read().decode('utf-8'))

    if 'launches' in rocketData:
        blast = rocketData['launches']
        b1 = blast[0]
        b2 = blast[1]
        b3 = blast[2]
        b4 = blast[3]
        b5 = blast[4]
        utc_zone = tz.tzutc()
        local_zone = tz.tzlocal()
        blast1UtcTime = datetime.datetime.strptime(b1['net'], '%B %d, %Y %H:%M:%S %Z')
        if blast1UtcTime.hour >= 22 or blast1UtcTime.hour == 0:
            blast1UtcTime = blast1UtcTime + datetime.timedelta(days=1)
        blast1UtcTime = blast1UtcTime.replace(tzinfo=utc_zone)
        blast1LocalString = str(blast1UtcTime.astimezone(local_zone))
        blast1LocalTime = datetime.datetime.strptime(blast1LocalString, '%Y-%m-%d %H:%M:%S+02:00')
        blast2UtcTime = datetime.datetime.strptime(b2['net'], '%B %d, %Y %H:%M:%S %Z')
        if blast2UtcTime.hour >= 22 or blast2UtcTime.hour == 0:
            blast2UtcTime = blast2UtcTime + datetime.timedelta(days=1)
        blast2UtcTime = blast2UtcTime.replace(tzinfo=utc_zone)
        blast2LocalString = str(blast2UtcTime.astimezone(local_zone))
        blast2LocalTime = datetime.datetime.strptime(blast2LocalString, '%Y-%m-%d %H:%M:%S+02:00')
        blast3UtcTime = datetime.datetime.strptime(b3['net'], '%B %d, %Y %H:%M:%S %Z')
        if blast3UtcTime.hour >= 22 or blast3UtcTime.hour == 0:
            blast3UtcTime = blast3UtcTime + datetime.timedelta(days=1)
        blast3UtcTime = blast3UtcTime.replace(tzinfo=utc_zone)
        blast3LocalString = str(blast3UtcTime.astimezone(local_zone))
        blast3LocalTime = datetime.datetime.strptime(blast3LocalString, '%Y-%m-%d %H:%M:%S+02:00')
        blast4UtcTime = datetime.datetime.strptime(b4['net'], '%B %d, %Y %H:%M:%S %Z')
        if blast4UtcTime.hour >= 22 or blast4UtcTime.hour == 0:
            blast4UtcTime = blast4UtcTime + datetime.timedelta(days=1)
        blast4UtcTime = blast4UtcTime.replace(tzinfo=utc_zone)
        blast4LocalString = str(blast4UtcTime.astimezone(local_zone))
        blast4LocalTime = datetime.datetime.strptime(blast4LocalString, '%Y-%m-%d %H:%M:%S+02:00')
        blast5UtcTime = datetime.datetime.strptime(b5['net'], '%B %d, %Y %H:%M:%S %Z')
        if blast5UtcTime.hour >= 22 or blast5UtcTime.hour == 0:
            blast5UtcTime = blast5UtcTime + datetime.timedelta(days=1)
        blast5UtcTime = blast5UtcTime.replace(tzinfo=utc_zone)
        blast5LocalString = str(blast5UtcTime.astimezone(local_zone))
        blast5LocalTime = datetime.datetime.strptime(blast5LocalString, '%Y-%m-%d %H:%M:%S+02:00')
        bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
        formattedlaunchInfo = 'Upcoming Rocket Launches:\n\n' + \
                                  str(blast1LocalTime) + \
                                  '\n*' + b1['name'] + \
                                  '*\nLaunching from [' + b1['location']['pads'][0]['name'] + '](' + b1['location']['pads'][0][
                                      'mapURL'] + ')' + \
                                  ('\nWatch live at ' + b1['vidURL'] if 'vidURL' in b1 else '') + '\n\n' + \
                                  str(blast2LocalTime) + \
                                  '\n*' + b2['name'] + \
                                  '*\nLaunching from [' + b2['location']['pads'][0]['name'] + '](' + b2['location']['pads'][0][
                                      'mapURL'] + ')' + \
                                  ('\nWatch live at ' + b2['vidURL'] if 'vidURL' in b2 else '') + '\n\n' + \
                                  str(blast3LocalTime) + \
                                  '\n*' + b3['name'] + \
                                  '*\nLaunching from [' + b3['location']['pads'][0]['name'] + '](' + b3['location']['pads'][0][
                                      'mapURL'] + ')' + \
                                  ('\nWatch live at ' + b3['vidURL'] if 'vidURL' in b3 else '') + '\n\n' + \
                                  str(blast4LocalTime) + \
                                  '\n*' + b4['name'] + \
                                  '*\nLaunching from [' + b4['location']['pads'][0]['name'] + '](' + b4['location']['pads'][0][
                                      'mapURL'] + ')' + \
                                  ('\nWatch live at ' + b4['vidURL'] if 'vidURL' in b4 else '') + '\n\n' + \
                                  str(blast5LocalTime) + \
                                  '\n*' + b5['name'] + \
                                  '*\nLaunching from [' + b5['location']['pads'][0]['name'] + '](' + b5['location']['pads'][0][
                                      'mapURL'] + ')' + \
                                  ('\nWatch live at ' + b5['vidURL'] if 'vidURL' in b5 else '')
        return bot.sendMessage(chat_id=chat_id, text=formattedlaunchInfo, parse_mode=telegram.ParseMode.MARKDOWN,
                               disable_web_page_preview=True)

    bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
    return bot.sendMessage(chat_id=chat_id, text='I\'m sorry ' + (user if not user == '' else 'Dave') +\
                                                 ', I\'m afraid I can\'t find any upcoming rocket launches.',
                           parse_mode=telegram.ParseMode.MARKDOWN,
                           disable_web_page_preview=True)

plugin_info = {
    'name': "Launch",
    'desc': "Gets info for the next few rocket launches."
}

arguments = {
    'text': [
        "(?i)^[\/](launch)"
    ]
}
