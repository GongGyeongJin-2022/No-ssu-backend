import requests
from No_ssu_backend.settings import get_env_variable


def send_push_message(user, data):
    if user.fcm_token is None:
        return
    headers = {
        'Authorization': f'key={get_env_variable("FCM_SERVER_KEY")}',
        'Content-Type': 'application/json'
    }
    body = {
        'to': user.fcm_token,
        'notification': data,
        'contentAvailable': 'true',
        'priority': 'high'
    }
    res = requests.post('https://fcm.googleapis.com/fcm/send', headers=headers, json=body)
