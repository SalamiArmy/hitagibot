import re

import util
from tgapi import TelegramApi


class RouteMessage:
    def __init__(self, message, misc, plugins, database, check_db_only=False):
        self.message = message
        self.misc = misc
        self.plugins = plugins
        self.database = database
        self.message['flagged_message'] = None
        self.message['matched_regex'] = None
        self.message['matched_argument'] = None
        if self.check_db() and not check_db_only:
            self.plugin_check()

    def check_db(self):
        chat_id = self.message['chat']['id']
        if 'text' in self.message:
            self.message['text'] = util.clean_message(self.message['text'], self.misc['bot_info']['username'])
        if 'reply_to_message' in self.message:
            message_id = self.message['reply_to_message']['message_id']
            db_selection = self.database.select("flagged_messages",
                                                ["plugin_id", "user_id", "single_use", "currently_active"],
                                                {"message_id": message_id, "chat_id": chat_id})
            if db_selection:
                for result in db_selection:
                    if result['user_id'] and result['user_id'] != self.message['from']['id']:
                        return True
                    if result['single_use']:
                        self.database.delete('flagged_messages', {'message_id': message_id, 'chat_id': chat_id})
                    self.message['flagged_message'] = True
                    self.plugins[result['plugin_id']].main(
                        TelegramApi(self.misc, self.database, result['plugin_id'], self.message))
                return False
        if self.message['chat']['type'] == 'private':
            if self.plugin_check():
                return False
            db_selection = self.database.select("flagged_messages",
                                                ["plugin_id", "single_use", "message_id"],
                                                {"chat_id": chat_id, "currently_active": True})
            if db_selection:
                for result in db_selection:
                    message_id = result["message_id"]
                    if result['single_use']:
                        self.database.delete('flagged_messages',
                                             {'message_id': message_id,
                                              'chat_id': chat_id})
                    self.message['flagged_message'] = True
                    self.plugins[result['plugin_id']].main(
                        TelegramApi(self.misc, self.database, result['plugin_id'], self.message)
                    )
                    self.database.update("flagged_messages", {"currently_active": False},
                                         {"chat_id": chat_id})
                return False
        return True

    def plugin_check(self):
        plugin_triggered = False
        for plugin in self.plugins:
            for key, value in plugin.arguments.items():
                if self.check_argument(key, value, self.message):
                    plugin_triggered = True
                    plugin.main(
                        TelegramApi(self.misc, self.database, self.plugins.index(plugin), self.message)
                    )
        return plugin_triggered

    def check_argument(self, key, value, incremented_message):
        if key in incremented_message:
            if type(value) is list:
                incremented_message = incremented_message[key]
                return self.check_match(key, value, incremented_message)
            elif type(value) is dict:
                incremented_message = incremented_message[key]
                for key1, value1 in value.items():
                    if self.check_argument(key1, value1, incremented_message):
                        return True
        else:
            return False

    def check_match(self, key, values, incremented_message):
        self.message['matched_argument'] = key
        if '*' in values:
            self.message['matched_regex'] = '*'
            return True
        for regex in values:
            match = re.findall(str(regex), str(incremented_message))
            if match:
                self.message['matched_regex'] = regex
                self.message['match'] = match[0]
                return True
        return False
