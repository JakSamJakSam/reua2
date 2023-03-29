from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
import requests

def send_email_to_staffs(subject, message='', html_message=''):
    recipients = [
        l[0] for
        l in get_user_model().objects.filter(is_staff=True, is_active=True ).exclude(email='').values_list('email')
    ]
    send_mail(subject, message, None, recipients, fail_silently=not settings.DEBUG, html_message=html_message)

def send_to_telegram(message):
    token = settings.TELEGRAM_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    if token is not None and chat_id is not None:
        data = {
            "chat_id": chat_id,
            "text": message,
        }
        r = requests.post(f'https://api.telegram.org/bot{token}/sendMessage', data=data)
        if r.status_code != 200:
            raise Exception("post_text error")
