import json
import os
import re
import shutil
import sys

import requests

from db import Database


class ConfigUtils:
    def __init__(self, filename='config.ini'):
        import configparser
        self.filename = filename
        self.config = configparser.ConfigParser()
        self.config.read(filename)
        self.token = self.config['BOT_CONFIG']['token']
        self.plugins = self.config['BOT_CONFIG']['plugins'].split(',')
        self.sleep = float(self.config['BOT_CONFIG']['sleep'])
        self.workers = int(self.config['BOT_CONFIG']['workers'])
        if self.config['BOT_CONFIG']['extensions']:
            self.extensions = self.config['BOT_CONFIG']['extensions'].split(',')
        else:
            self.extensions = list()

    def write_config(self):
        with open(self.filename, 'w') as configfile:
            self.config.write(configfile)


def post(content, session=requests):
    response = session.post(**content)
    return response


def fetch(url, session=requests):  # Grabs from url and parses as json. note2self, don't make it parse json by default
    try:
        response = session.get(url, timeout=3)
        return response
    except requests.exceptions.ReadTimeout:
        return 'Request timed out :('
    except requests.exceptions.ConnectionError:
        return 'Unable to connect :('


def fetch_file(url, file_path, session=requests):
    response = session.get(url, stream=True)
    with open(file_path, 'wb') as out_file:
        response.raw.decode_content = True
        shutil.copyfileobj(response.raw, out_file)
    return file_path


def clean_message(message, bot_name):  # Replace this with something based on MessageEntities
    bot_name = '@' + bot_name
    name_match = re.search('^(/[^ ]*){}'.format(bot_name), message)
    if name_match:
        return message.replace(message[:name_match.end(0)], message[:name_match.end(0) - len(bot_name)])
    else:
        return message


def name_file(file_id, file_name):
    if file_name:
        match = re.findall('(\.[0-9a-zA-Z]+$)', file_name)
        if match:
            return file_id + match[0]
    return str(file_id)


def init_package(config):  # Creates the package that's passed around, replaced eventually probably
    session = requests.session()  # Creates session, used for ALL requests to telegram
    bot_info = get_me(config.token, session)  # this stores the getMe object
    database = init_db()  # Stores the database object
    plugins = init_plugins(database, config.plugins)  # Stores all plugins
    misc = {
        "token": config.token, "bot_info": bot_info, "session": session
    }
    extensions = init_extension(config.extensions)
    return [misc, plugins, database, extensions]


def init_db():  # Creates the DB object and sets up hierarchy
    if not os.path.exists('data'):  # All data should be placed here
        os.makedirs('data/files')
    db = Database('bot')
    db.create_table("plugins", {"plugin_id": "INT PRIMARY KEY NOT NULL", "plugin_name": "TEXT",
                                "pretty_name": "TEXT", "description": "TEXT", "usage": "TEXT"}, drop_existing=True)
    db.create_table("flagged_messages", {"plugin_id": "INT", "message_id": "INT", "chat_id": "INT",
                                         "user_id": "INT", "single_use": "BOOLEAN", "currently_active": "BOOLEAN",
                                         "plugin_data": "TEXT"})
    db.create_table("flagged_time", {"plugin_id": "INT", "time": "INT", "plugin_data": "TEXT"})
    db.create_table("downloads", {"file_id": "TEXT", "file_path": "TEXT"})
    db.create_table("callback_queries", {"plugin_id": "INT", "data": "TEXT", "plugin_data": "TEXT"})
    return db


def init_plugins(db, plugin_list):
    plugins = list()
    for plugin_id, plugin_name in enumerate(plugin_list):  # Read plugins from the config file
        try:
            plugin = __import__('plugins', fromlist=[plugin_name])  # Import it from the plugins folder
            plugins.append(getattr(plugin, plugin_name))  # Stores plugin objects in a dictionary
        except AttributeError:
            print("X - Unable to load plugin {}".format(plugin_name))
            continue
        if 'name' not in plugins[plugin_id].plugin_info:  # Check for name in plugin arguments
            plugins[plugin_id].plugin_info['name'] = plugin_name
        pretty_name = plugins[plugin_id].plugin_info['name']
        if 'desc' not in plugins[plugin_id].plugin_info:  # Check for description in plugin arguments
            plugins[plugin_id].plugin_info['desc'] = None
        description = plugins[plugin_id].plugin_info['desc']
        if 'usage' not in plugins[plugin_id].plugin_info:  # Check for usage in plugin arguments
            plugins[plugin_id].plugin_info['usage'] = None
        usage = json.dumps(plugins[plugin_id].plugin_info['usage'])  # Stores usage as json
        db.insert("plugins", {"plugin_id": plugin_id, "plugin_name": plugin_name, "pretty_name": pretty_name,
                              "description": description, "usage": usage})  # Insert plugin into DB
        print("✓ - Loaded plugin {}".format(plugin_name))
    return tuple(plugins)


def init_extension(extensions_list):
    extensions = dict()
    for extension_name in extensions_list:
        try:
            extension = __import__('extensions', fromlist=[extension_name])
            extensions.update({
                extension_name: {
                    'module': getattr(extension, extension_name),
                    'data': None
                }
            })
        except AttributeError:
            print("X - Unable to load extension {}".format(extension_name))
            continue
        print("✓ - Loaded extension {}".format(extension_name))
    return extensions


def get_me(token, session):  # getMe
    url = "https://api.telegram.org/bot{}/getMe".format(token)  # Set url for getMe
    response = fetch(url, session).json()
    if response['ok']:
        print("{} - @{}\n".format(response['result']['first_name'], response['result']['username']))
        return response['result']
    else:  # Usually means the token is wrong
        print('Error fetching bot info\nResponse: {}\nShutting Down'.format(response))
        sys.exit()
