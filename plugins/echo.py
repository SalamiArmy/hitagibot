def main(tg):
    tg.send_chat_action('typing')
    if tg.message['flagged_message']:
        if 'text' in tg.message:
            tg.send_message(tg.message['text'])
        else:
            tg.send_message("I only echo text :(")
    elif 'reply_to_message' in tg.message:
        tg.send_message(tg.message['reply_to_message']['text'])
    elif tg.message['matched_regex'] == arguments['text'][0]:
        tg.send_message("What do I echo?", flag_message=True)
    elif tg.message['matched_regex'] == arguments['text'][1]:
        tg.send_message(tg.message['match'][1])


plugin_info = {
    'name': "Echo",
    'desc': "The echo plugin repeats your message text",
    'usage': [
        "/echo"
    ],
}

arguments = {
    'text': [
        "^[/]echo$",
        "(?i)^[\/](echo) (.*)"
    ]
}
