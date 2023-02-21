from django.forms import Form, CharField, EmailField, TextInput
from django.utils.translation import gettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField

class FeedbackForm(Form):
    fio = CharField(max_length=100, required=True, label=_("Ім'я"))
    phone = PhoneNumberField(required=True, label=_("Номер телефону"))
    email = EmailField(required=True, label="E-Mail")
    message = CharField(required=True, label=_("Повідомлення"), widget=TextInput)
