import json
import requests


SLACK_WEBHOOKS = {
    'order-purchased':
        {
            'webhook': ('https://hooks.slack.com/services/T05SLPAV75K/B05TCM0'
                        'CGKS/YDb4fVRnPO40XKEoX0nv7jTc'),
            'botname': 'OrderBot'
        }
}


def send_slack_notification(channel_name, message):
    if message:
        try:
            slack_config = SLACK_WEBHOOKS.get(channel_name)
            webhook_url = slack_config.get('webhook')
            user_name = slack_config.get('botname')
            payload = {
                'text': message,
                'username': user_name}
            data = json.dumps(payload)
            requests.post(webhook_url, data)
        except Exception as ex:
            print("exception occured while sending slack", ex)
