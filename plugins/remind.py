def main(tg):
    tg.send_chat_action('typing')
    if tg.plugin_data:
        tg.send_message("You asked me to remind you at this time")
    elif tg.message['flagged_message']:
        if 'text' in tg.message:
            tg.send_message("Ok I will remind you in {} minute(s)".format(tg.message['text']))
            tg.flag_time(**add_entry(int(tg.message['text'])))
    elif tg.message['matched_regex'] == arguments['text'][0]:
        tg.send_message("In how many minutes would you like to be reminded?", flag_message=True)


def add_entry(response_time):
    import time
    time = time.time() + (response_time * 60)
    package = {
        'time': time
    }
    return package


plugin_info = {
    'name': "Remind",
    'desc': "The remind plugin gives you a notification at the time you specify",
    'usage': [
        "/remind"
    ],
}

arguments = {
    'text': [
        "^[/]remind$"
    ]
}
