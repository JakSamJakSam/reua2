from django import forms
from django_summernote.widgets import SummernoteWidget

from reua.models import TopMenu, News


class TopMenuAdminForm(forms.ModelForm):
    ALLOWED_URL_NAMES = (
        'company-list', 'investition-list', 'water',
        'about', 'rebuild', 'contacts', 'news-list',
    )

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


# smnt = {}
# class NewsAdminForm(forms.ModelForm):
#     body = forms.CharField(widget=SummernoteWidget(attrs=smnt))
#     class Meta:
#         model = News
#         fields = '__all__'
