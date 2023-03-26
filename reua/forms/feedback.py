from django.forms import ModelForm
from reua.models import FeedbackMessage


class FeedbackForm(ModelForm):
    class Meta:
        model = FeedbackMessage
        fields = '__all__'

