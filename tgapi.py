from functools import partial

import util
import json


class TelegramApi:
    def __init__(self, misc, database, plugin_id, message=None, plugin_data=None, callback_query=None):
        self.message = message
        self.misc = misc
        self.database = database
        self.plugin_id = plugin_id
        self.plugin_data = plugin_data
        self.callback_query = callback_query
        self.send_photo = partial(self.send_file, 'sendPhoto')
        self.send_audio = partial(self.send_file, 'sendAudio')
        self.send_document = partial(self.send_file, 'sendDocument')
        self.send_sticker = partial(self.send_file, 'sendFile')
        self.send_video = partial(self.send_file, 'sendVideo')
        self.send_voice = partial(self.send_file, 'sendVoice')
        self.get_chat = partial(self.get_something, 'getChat')
        self.get_chat_administrators = partial(self.get_something, 'getChatAdministrators')
        self.get_chat_members_count = partial(self.get_something, 'getChatMembersCount')
        self.edit_message_reply_markup = partial(self.edit_content, 'editMessageReplyMarkup')
        self.reply_keyboard_hide = reply_keyboard_hide
        self.reply_keyboard_markup = reply_keyboard_markup
        self.force_reply = force_reply
        if self.message:
            self.chat_data = self.message
        elif self.callback_query:
            self.chat_data = self.callback_query['message']
        else:
            self.chat_data = self.plugin_data['prev_message']

    def method(self, method_name, check_content=True, **kwargs):
        content = dict()
        content['data'] = dict()
        content['url'] = 'https://api.telegram.org/bot{}/{}'.format(self.misc['token'], method_name)
        if check_content:
            if self.chat_data['chat']['type'] != 'private':
                content['data'].update({'reply_to_message_id': self.chat_data['message_id']})
            if 'chat_id' not in kwargs:
                content['data'].update({'chat_id': self.chat_data['chat']['id']})
            if 'file' in kwargs:
                content['files'] = kwargs.pop('file')
        content['data'].update(kwargs)
        response = util.post(content, self.misc['session']).json()
        if not response['ok']:
            print('Error with response\nResponse: {}\nSent: {}'.format(response, content))
        return response

    def get_something(self, method, chat_id=None):
        chat_id = chat_id or self.message['chat']['id']
        return self.method(method, check_content=False, chat_id=chat_id)

    def send_message(self, text, flag_message=None, **kwargs):
        arguments = {'text': text, 'parse_mode': 'HTML'}
        arguments.update(kwargs)
        response = self.method('sendMessage', **arguments)
        if flag_message and response['ok']:  # Will crash if response attribute error
            message_id = response['result']['message_id']
            if type(flag_message) is dict and 'message_id' not in flag_message:
                flag_message.update({'message_id': int(message_id)})
            else:
                flag_message = message_id
            self.flag_message(flag_message)
        return response

    def forward_message(self, message_id, **kwargs):
        package = kwargs
        package.update({'message_id': message_id})
        if 'chat_id' not in package:
            chat_id = self.chat_data['chat']['id']
            package.update({'chat_id': chat_id})
        return self.method('sendMessage', **package)

    def send_file(self, method, file, **kwargs):
        arguments = kwargs
        arguments.update({'file': file})
        return self.method(method, **arguments)

    def send_location(self, latitude, longitude, **kwargs):
        arguments = locals()
        del arguments['self']
        arguments.update(arguments.pop('kwargs'))
        return self.method('sendLocation', **arguments)

    def send_venue(self, latitude, longitude, title, address, **kwargs):
        arguments = locals()
        del arguments['self']
        arguments.update(arguments.pop('kwargs'))
        return self.method('sendVenue', **arguments)

    def send_contact(self, phone_number, first_name):
        arguments = locals()
        del arguments['self']
        arguments.update(arguments.pop('kwargs'))
        return self.method('sendContact', **arguments)

    def send_chat_action(self, action, **kwargs):
        arguments = locals()
        del arguments['self']
        arguments.update(arguments.pop('kwargs'))
        return self.method('sendChatAction', **arguments)

    def get_user_profile_photos(self, user_id, offset=0, limit=0):
        arguments = locals()
        del arguments['self']
        return self.method('getUserProfilePhotos', check_content=False, **arguments)

    def get_file(self, file_id):
        return self.method('getFile', check_content=False, file_id=file_id)

    def kick_chat_member(self, user_id, chat_id=None):
        arguments = locals()
        del arguments['self']
        if not arguments['chat_id']:
            del arguments['chat_id']
        return self.method('kickChatMember', **arguments)

    def unban_chat_member(self, user_id, chat_id=None):
        arguments = locals()
        del arguments['self']
        if not arguments['chat_id']:
            del arguments['chat_id']
        return self.method('unbanChatMember', **arguments)

    def answer_callback_query(self, text=None, callback_query_id=None, show_alert=False):
        arguments = locals()
        del arguments['self']
        if not callback_query_id:
            try:
                arguments.update({'callback_query_id': int(self.callback_query['id'])})
            except KeyError:
                return "Callback query ID not found!"
        return self.method('answerCallbackQuery', check_content=False, **arguments)

    def edit_content(self, method, **kwargs):
        arguments = kwargs
        if 'chat_id' and 'inline_message_id' not in arguments:
            if 'message_id' in arguments:
                chat_id = self.chat_data['chat']['id']
                arguments.update({'chat_id': chat_id})
            else:
                return 'ERROR: Need chat_id + message_id or inline_message_id'
        return self.method(method, check_content=False, **arguments)

    def edit_message_text(self, text, **kwargs):
        arguments = locals()
        del arguments['self']
        arguments.update(arguments.pop('kwargs'))
        return self.edit_content('editMessageText', **arguments)

    def edit_message_caption(self, **kwargs):
        if 'caption' and 'reply_markup' not in kwargs:
            return 'ERROR: Need caption or reply_markup'
        return self.edit_content('editMessageText', **kwargs)

    def flag_message(self, parameters):
        chat_id = self.chat_data['chat']['id']
        default = {"plugin_id": self.plugin_id, "single_use": False, "currently_active": True,
                   "chat_id": chat_id, "user_id": None}
        if type(parameters) is dict:
            if 'chat_id' in parameters:
                chat_id = parameters['chat_id']
            if 'plugin_data' in parameters:
                default['plugin_data'] = json.dumps(parameters.pop('plugin_data'))
            default.update(parameters)
        elif type(parameters) is int:
            default.update({"message_id": parameters})
        self.database.update("flagged_messages", {"currently_active": False}, {"chat_id": chat_id})
        self.database.insert('flagged_messages', default)

    def flag_time(self, time, plugin_data=None, plugin_id=None):
        if not plugin_id:
            plugin_id = self.plugin_id
        default = {"prev_message": self.chat_data}
        if plugin_data and type(plugin_data) is dict:
            default.update(plugin_data)
        self.database.insert("flagged_time",
                             {"plugin_id": plugin_id, "time": time, "plugin_data": json.dumps(default)})

    def download_file(self, file_object):
        if file_object['ok'] and file_object['result']['file_size'] < 20000000:
            file_object = file_object['result']
        else:
            print("Unable to download file\nObject received: {}".format(file_object))
            return
        db_selection = self.database.select("downloads", ["file_path"], {"file_id": file_object["file_id"]})
        if db_selection:
            return db_selection[0]['file_path']
        else:
            url = "https://api.telegram.org/file/bot{}/{}".format(self.misc['token'], file_object['file_path'])
            try:
                name = file_object['file_path']
            except KeyError:
                name = None
            file_name = util.name_file(file_object['file_id'], name)
            self.database.insert("downloads", {"file_id": file_object["file_id"],
                                               "file_path": "data/files/{}".format(file_name)})
            return util.fetch_file(url, 'data/files/{}'.format(file_name), self.misc['session'])

    def inline_keyboard_markup(self, list_of_list_of_buttons, plugin_data=None):
        for button_list in list_of_list_of_buttons:
            for button in button_list:
                if 'text' not in button:
                    return "Error: Text not found in button object"
                if 'callback_data' in button:
                    self.database.insert("callback_queries",
                                         {"plugin_id": self.plugin_id, "data": button['callback_data'],
                                          "plugin_data": plugin_data})
        package = {
            'inline_keyboard': list_of_list_of_buttons
        }
        return json.dumps(package)

    def get_chat_member(self, user_id, chat_id=None):
        chat_id = chat_id or self.message['chat']['id']
        return self.method('getChatMember', check_content=False, user_id=user_id, chat_id=chat_id)


def reply_keyboard_markup(list_of_list_of_buttons, resize_keyboard=False, one_time_keyboard=False,
                          selective=False):
    for button_list in list_of_list_of_buttons:
        for button in button_list:
            if 'text' not in button:
                return "Error: Text not found in button object"
    package = {
        'keyboard': list_of_list_of_buttons,
        'resize_keyboard': resize_keyboard,
        'one_time_keyboard': one_time_keyboard,
        'selective': selective
    }
    return json.dumps(package)


def reply_keyboard_hide(hide_keyboard=True, selective=False):
    package = {
        'hide_keyboard': hide_keyboard,
        'selective': selective
    }
    return json.dumps(package)


def force_reply(forced_reply=True, selective=False):
    package = {
        'force_reply': forced_reply,
        'selective': selective
    }
    return json.dumps(package)
