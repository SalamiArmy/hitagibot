import random


def main(tg):
    tg.send_chat_action('typing')
    if tg.plugin_data:
        tg.send_message("Reminder:\n{}".format(tg.plugin_data['message']))
    elif tg.message['matched_regex']:
        package, message = add_entry(tg.message['match'][1], tg.message['match'][2], tg.message['match'][3])
        tg.flag_time(**package)
        tg.send_message(message)


def add_entry(response_time, unit, message):
    import time
    if message[0:3] == 'to ':
        message = message[3:]
    responses = ["Ok, I will remind you in", "I'll be sure to remind you in", "Expect to hear from me in",
                 "I'll be sure to ping you in"]
    response_time = int(response_time)
    epoch_time = 0
    response = "{} {} ".format(random.choice(responses), response_time)
    if unit.lower() == 's' or 'second' in unit:
        epoch_time = response_time
        response += 'second'
    elif unit.lower() == 'm' or 'minute' in unit:
        epoch_time = response_time * 60
        response += 'minute'
    elif unit.lower() == 'h' or 'hour' in unit:
        epoch_time = response_time * 60 * 60
        response += 'hour'
    if response_time > 1:
        response += 's'
    time = time.time() + epoch_time
    package = {
        'time': time,
        'plugin_data': {
            'message': message
        }
    }
    return [package, response]


plugin_info = {
    'name': "Remind",
    'desc': "The remind plugin gives you a notification at the time you specify",
    'usage': [
        'Example: "Remind me in 50 minutes to get off telegram!"'
    ],
}

arguments = {
    'text': [
        "(?i)(remind) .* (\d+)([smd]) (.*)",
        "(?i)(remind) .* (\d+) (seconds|minutes|hours) (.*)",
        "(?i)(remind) .* (\d+) (second|minute|hour) (.*)",
    ]
}
