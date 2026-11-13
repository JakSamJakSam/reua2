from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Case, When, Value
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from reua.forms.feedback import FeedbackForm, FeedbackFormGCaptcha
from reua.models import TopMenu, FoundingDocument, SiteSettings, BankTransferAttributes
from reua.models.projects import currencies, KindProject


def top_menus(request):
    site = get_current_site(request)
    ss = SiteSettings.objects.get(site=site)
    return {
        'top_menu_items': TopMenu.objects.filter(disabled=False, parent=None).order_by('order'),
        'founding_documents': FoundingDocument.objects.all(),
        'site_settings': ss,
        'google_data_stream_id': settings.GOOGLE_DATA_STREAM_ID,
        'google_recaptcha_key': settings.GOOGLE_RECAPTCHA_KEY,
        'feedback_form': FeedbackForm() if settings.GOOGLE_RECAPTCHA_KEY is None else FeedbackFormGCaptcha() ,
    }
