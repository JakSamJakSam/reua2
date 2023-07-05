from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Case, When, Value
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from reua.forms.feedback import FeedbackForm
from reua.models import TopMenu, FoundingDocument, SiteSettings, BankTransferAttributes
from reua.models.projects import currencies, KindProject


def top_menus(request):
    site = get_current_site(request)
    bta = BankTransferAttributes.objects.annotate(
        order=Case(
            *[When(currency=v, then=Value(i)) for i, v in enumerate(currencies.keys())],
            default=99,
        ),
    ).order_by('order')
    return {
        'top_menu_items': TopMenu.objects.filter(disabled=False).order_by('order'),
        'founding_documents': FoundingDocument.objects.all(),
        'site_settings': SiteSettings.objects.get(site=site),
        'google_data_stream_id': settings.GOOGLE_DATA_STREAM_ID,
        'payments': {
            'reH2O': {
                'title': _("Питна вода"),
                'bank': bta.filter(kind=KindProject.water.value),
                'credit_card': reverse('Pay_ReH2O'),
                'crypto': settings.PAYMENT_CRYPTO_RE_H2O,
            },
            'reCity': {
                'title': _("Відбудова житла"),
                'bank': bta.filter(kind=KindProject.city.value),
                'credit_card': reverse('Pay_ReCity'),
                'crypto': settings.PAYMENT_CRYPTO_RE_CITY,
            },
        },
        'feedback_form': FeedbackForm(),
    }
