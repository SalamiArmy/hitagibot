import re
import json
import time
from tgapi import TelegramApi


class RouteMessage:
    def __init__(self, message, misc, plugins, database):
        self.message = message
        self.misc = misc
        self.plugins = plugins
        self.database = database
        self.message['flagged_message'] = None
        self.message['matched_regex'] = None
        self.message['matched_argument'] = None

    def route_update(self):
        if 'reply_to_message' in self.message and not self.check_db_reply():
            self.plugin_check()
        elif self.message['chat']['type'] == 'private':
            self.check_db_pm()
        else:
            self.plugin_check()

    def check_db_reply(self):
        chat_id = self.message['chat']['id']
        message_id = self.message['reply_to_message']['message_id']
        db_selection = self.database.select("flagged_messages",
                                            ["DISTINCT plugin_id", "user_id", "single_use", "currently_active",
                                             "plugin_data"],
                                            {"message_id": message_id, "chat_id": chat_id})
        if db_selection:
            for result in db_selection:
                if result['user_id'] and result['user_id'] != self.message['from']['id']:
                    return True
                if result['single_use']:
                    self.database.delete('flagged_messages', {'message_id': message_id, 'chat_id': chat_id})
                self.message['flagged_message'] = True
                if result['plugin_data']:
                    plugin_data = json.loads(result['plugin_data'])
                else:
                    plugin_data = None
                self.plugins[result['plugin_id']].main(
                    TelegramApi(self.misc, self.database, result['plugin_id'], self.message, plugin_data))
            return True

    def check_db_pm(self):
        if self.plugin_check():
            return
        chat_id = self.message['chat']['id']
        db_selection = self.database.select("flagged_messages",
                                            ["DISTINCT plugin_id", "single_use", "message_id", "plugin_data"],
                                            {"chat_id": chat_id, "currently_active": True})
        if db_selection:
            for result in db_selection:
                message_id = result["message_id"]
                if result['single_use']:
                    self.database.delete('flagged_messages',
                                         {'message_id': message_id,
                                          'chat_id': chat_id})
                if result['plugin_data']:
                    plugin_data = json.loads(result['plugin_data'])
                else:
                    plugin_data = None
                self.message['flagged_message'] = True
                self.database.update("flagged_messages", {"currently_active": False},
                                     {"chat_id": chat_id})
                self.plugins[result['plugin_id']].main(
                    TelegramApi(self.misc, self.database, result['plugin_id'], self.message, plugin_data)
                )

    def plugin_check(self):
        if int(time.time()) - int(self.message['date']) >= 180:
            return False
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


def route_callback_query(callback_query, database, plugins, misc):
    if int(time.time()) - int(callback_query['message']['date']) >= 30:
        return
    db_selection = database.select("callback_queries", ["DISTINCT plugin_id", "plugin_data", "data"],
                                   {"data": callback_query['data']})
    for db_result in db_selection:
        plugin_id = db_result['plugin_id']
        plugin_data = json.loads(db_result['plugin_data']) if db_result['plugin_data'] else None
        api_obj = TelegramApi(misc, database, plugin_id, plugin_data=plugin_data,
                              callback_query=callback_query)
        plugins[plugin_id].main(api_obj)
