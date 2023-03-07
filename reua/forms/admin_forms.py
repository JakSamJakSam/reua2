from django import forms
from reua.models import TopMenu

class TopMenuAdminForm(forms.ModelForm):
    ALLOWED_URL_NAMES = ('company-list', 'investition-list', 'water', 'about', 'rebuild', 'contacts')

    url_name = forms.ChoiceField(
        choices=(
            (None, '-'),
            *((n, n) for n in ALLOWED_URL_NAMES)
        ),
        required=False,
    )

    class Meta:
        model = TopMenu
        fields = '__all__'