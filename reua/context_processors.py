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
    bta = BankTransferAttributes.objects.annotate(
        order=Case(
            *[When(currency=v, then=Value(i)) for i, v in enumerate(currencies.keys())],
            default=99,
        ),
    ).order_by('order')
    return {
        'top_menu_items': TopMenu.objects.filter(disabled=False, parent=None).order_by('order'),
        'founding_documents': FoundingDocument.objects.all(),
        'site_settings': SiteSettings.objects.get(site=site),
        'google_data_stream_id': settings.GOOGLE_DATA_STREAM_ID,
        'google_recaptcha_key': settings.GOOGLE_RECAPTCHA_KEY,
        'payments': {
            'reH2O': {
                'title': _("Питна вода"),
                'desc': _("Благодійний внесок на виготовлення мобільних систем очищення води для зруйнованих міст та селищ України, та забезпечення статутної діяльності фонду"),
                'bank': bta.filter(kind=KindProject.water.value),
                'credit_card': reverse('Pay_ReH2O'),
                'credit_cards': settings.PAYMENT_CARD_RE_H2O,
                'crypto': settings.PAYMENT_CRYPTO_RE_H2O,
                'key': 'reh20',
            },
            'reCity': {
                'title': _("Відбудова житла"),
                'desc': _("Благодійний внесок на виготовлення мобільних систем очищення води для зруйнованих міст та селищ України, та забезпечення статутної діяльності фонду"),
                'bank': bta.filter(kind=KindProject.city.value),
                'credit_card': reverse('Pay_ReCity'),
                'credit_cards': settings.PAYMENT_CARD_RE_CITY,
                'crypto': settings.PAYMENT_CRYPTO_RE_CITY,
                'key': 'city',
            },
        },
        'feedback_form': FeedbackForm() if settings.GOOGLE_RECAPTCHA_KEY is None else FeedbackFormGCaptcha() ,
    }
