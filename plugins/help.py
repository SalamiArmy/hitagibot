import json
import random


def main(tg):
    tg.send_chat_action('typing')
    if tg.message['flagged_message']:
        tg.send_message(grab_plugin(tg, chance=True))
    elif tg.message['matched_regex'] == arguments['text'][0]:
        plugin_list = tg.database.select("plugins", ["pretty_name"])
        message = "Here are a list of my plugins:"
        for plugin in plugin_list:
            for plugin_name in plugin.values():
                message += "\n<b>• {}</b>".format(plugin_name)
        message += "\n\nWhich plugin do you want more info on?"
        tg.send_message(message, flag_message=True)
    elif tg.message['matched_regex'] == arguments['text'][1]:
        tg.send_message(grab_plugin(tg, match=True))


def grab_plugin(tg, chance=False, match=False):
    message = "I couldn't find this plugin :("
    if match:
        plugin = tg.message['match'][1]
    else:
        plugin = tg.message['text']
    plugin_data = tg.database.select("plugins", ["pretty_name", "description", "usage"],
                                     {"lower(pretty_name)": plugin.lower()})
    for info in plugin_data:
        message = '<b>{}:</b>\n<pre>{}</pre>'.format(info['pretty_name'], info['description'])
        if info['usage'] != 'null':
            message += '\n<b>Usage:</b>'
            for i in json.loads(info['usage']):
                message += '\n<pre>{}</pre>'.format(i)
        if chance:
            chance = (random.randint(1, 5))
            if chance > 3:
                message += '\n\n<b>Tip:</b> You can also use <code>/help plugin-name</code>'
    return message


plugin_info = {
    'name': "Help",
    'desc': "Provides descriptions and usage for plugins you choose",
    'usage': [
        "/help"
    ],
}

arguments = {
    'text': [
        "^[/]help$",
        "(?i)^[\/](help) (.*)"
    ]
}
