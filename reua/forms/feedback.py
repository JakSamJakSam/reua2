from captcha.fields import CaptchaField, CaptchaTextInput
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from reua.models import FeedbackMessage

class FeedbackForm(ModelForm):
    def is_valid(self):
        v = super().is_valid()
        if not v and self.errors['captcha']:
            self.fields['captcha'].widget.attrs['class'] += ' is-invalid '
        return v

    captcha = CaptchaField(
        label=_('Введіть код з картинки'),
        widget=CaptchaTextInput(attrs={'class': "form-control bg-white border-0 border-bottom my-2"})
    )
    class Meta:
        model = FeedbackMessage
        fields = '__all__'

