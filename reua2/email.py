from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

def send_email_to_staffs(subject, message='', html_message=''):
    recipients = list(get_user_model().objects.filter(is_staff=True, is_active=True ).exclude(email='').values_list('email'))
    send_mail(subject, message, None, recipients, fail_silently=not settings.DEBUG, html_message=html_message)
