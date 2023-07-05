from captcha.fields import CaptchaField, CaptchaTextInput
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from reua.models import FeedbackMessage

class FeedbackForm(ModelForm):
    captcha = CaptchaField(
        label=_('Введіть код з картинки'),
        widget=CaptchaTextInput(attrs={'class': "form-control bg-white border-0 border-bottom my-2"})
    )
    class Meta:
        model = FeedbackMessage
        fields = '__all__'

