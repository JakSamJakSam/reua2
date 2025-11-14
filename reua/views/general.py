import qrcode
import qrcode.image.svg
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Case, When, Value
from django.template.loader import get_template
from django.templatetags.static import static
from django.urls import reverse
from django.views.generic import TemplateView, FormView, DetailView
from django.utils.translation import gettext_lazy as _
from qrcode.image.styles.moduledrawers.svg import *

from reua.forms.feedback import FeedbackForm, FeedbackFormGCaptcha
from reua.models import Partner, Staff, WaterStation, Project, FoundingDocument

__all__ = ('IndexView', 'FeedbackFormView', "AboutView", "WaterView", "RebuildView", "ContactsView", "FileView",
           'ReH2OPaymentView', 'ReCityPaymentView',
           'ReH2OPaymentNewView', 'ReCityPaymentNewView')

from reua.models.projects import KindProject, currencies, kind_project_values
from reua.models.site_models import GeneralProjectImages, ReH2OSettings, ReH2OVideos, BankTransferAttributes, \
    SiteSettings
from reua.models.waters import ActivePoints

from reua.views.mixins import BreadCrumbsMixin
from reua2.send_message import send_email_to_staffs, send_to_telegram


class IndexView(TemplateView):
    template_name = 'index/index.html'
    positions = {
        'top': GeneralProjectImages.POSITION_TOP,
        'bottom': GeneralProjectImages.POSITION_BOTTOM
    }


    def get_context_data(self, **kwargs):
        def get_qrcode(url, color):
            qr = qrcode.QRCode()
            qr.add_data(url)
            image_factory = qrcode.image.svg.SvgPathImage
            image_factory.QR_PATH_STYLE.update({
                'fill': 'white'
            })
            return qr.make_image(
                image_factory=image_factory,
                module_drawer=SvgPathCircleDrawer(),
            ).to_string(encoding='unicode')

        ctx = super().get_context_data(**kwargs)
        ctx['partners'] = Partner.objects.all()
        ctx['general_project_images'] = {
            project_name: {
                position_name: GeneralProjectImages.objects.filter(kind=project_key, position=position_key)[:3]
                for position_name, position_key in self.positions.items()
            }
            for project_key, project_name in reversed(kind_project_values.items())
        }
        # qrcodes = {
        #     'reH2O': {'url': reverse('Pay_ReH2O'), 'color': 'var(--main-blue'},
        #     'reCity': {'url': reverse('Pay_ReCity'), 'color': 'var(--main-yellow'},
        # }
        qrcodes = {
            'reH2O': {'url': 'https://qp.payhub.com.ua/#/payment/c-103415', 'color': 'var(--main-blue'},
            'reCity': {'url': 'https://qp.payhub.com.ua/#/payment/c-103416', 'color': 'var(--main-yellow'},
        }
        for k in qrcodes.keys():
            qrcodes[k]['img'] = get_qrcode(
                self.request.build_absolute_uri(qrcodes[k]['url']),
                qrcodes[k]['color']
            )
        ctx['qrcodes']=qrcodes

        return ctx


class FeedbackFormView(FormView):
    form_class = FeedbackForm
    template_name = 'feedback.html'

    def get_form_class(self):
        if settings.GOOGLE_RECAPTCHA_KEY is not None:
            return FeedbackFormGCaptcha
        return FeedbackForm

    def form_valid(self, form):
        template = get_template('email/feedback.html')
        html = template.render(form.cleaned_data)
        send_email_to_staffs(_('Отримано повідомлення'), html_message=html)
        tg_template = get_template('email/feedback.txt')
        tg_message = tg_template.render(form.cleaned_data)
        send_to_telegram(tg_message)
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        result = super().get_context_data(**kwargs)
        result['feedback_form'] = result['form']
        del result['form']
        return result

    def get_success_url(self):
        return reverse('index')


class AboutView(BreadCrumbsMixin, TemplateView):
    bc = [{'title': _("Про фонд")}]
    page_title = _("Хто ми?")
    template_name = "pages/about.html"

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['staffs'] = Staff.objects.all()
        ctx['partners'] = Partner.objects.all()
        return ctx


class WaterView(BreadCrumbsMixin, TemplateView):
    bc = [{'title': _("Питна вода")}]
    page_title = _("Питна вода")
    template_name = "pages/water.html"

    def get_water_stations(self):
        qs = WaterStation.objects.all()
        return [{
            'id': m.id,
            'lat': m.lat,
            'lng': m.lng,
            'title': m.localized_title,
            'desc': m.localized_desc,
            'marker': static("reua/img/water/marker.png"),

        } for m in qs
        ]

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['water_stations'] = self.get_water_stations()
        ctx['projects'] = Project.objects.filter(kind=KindProject.water.value)
        return ctx


class WaterNewView(BreadCrumbsMixin, TemplateView):
    bc = [{'title': _("Питна вода")}]
    page_title = _("Питна вода")
    template_name = "pages/water_new.html"

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        site = get_current_site(self.request)
        settings = ReH2OSettings.objects.filter(site=site).first()
        videos = ReH2OVideos.objects.filter(site=site)
        projects = Project.objects.filter(kind=KindProject.water.value)
        ctx['page_settings'] = settings
        ctx['videos'] = videos
        ctx['projects'] = projects
        ctx['map_points'] = [mp.point for mp in ActivePoints.objects.filter(active=True)]
        return ctx


class RebuildView(BreadCrumbsMixin, TemplateView):
    bc = [{'title': _("Відбудова")}]
    page_title = _("Відбудова житла")
    template_name = "pages/rebuild.html"


class ContactsView(BreadCrumbsMixin, TemplateView):
    bc = [{'title': _("Контакти")}]
    page_title = _("Контакти")
    template_name = "pages/contacts.html"


class FileView(BreadCrumbsMixin, DetailView):
    queryset = FoundingDocument.objects.filter(kind=FoundingDocument.KIND_PDF)
    context_object_name = 'document'
    template_name = "pages/pdf_file.html"

    def get_page_title(self):
        return self.object.localized_title

    def render_to_response(self, context, **response_kwargs):
        headers = {
            "X-Frame-Options": "SAMEORIGIN"
        }
        return super().render_to_response(context, headers=headers, **response_kwargs)


class ReH2OPaymentView(BreadCrumbsMixin, TemplateView):
    bc = [{'title': _("Зробити внесок")}]
    page_title = "ReH2O"
    template_name = "payment/basic.html"

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['title'] = _('Дякуємо, що ви готові підтримати наш проект з чистої води для мешканців України!')
        ctx['credit_cards'] = [{
            'url': url,
            'currency': cur,
            'currency_sign': currencies[cur] if cur in currencies else ''
        } for cur, url in settings.PAYMENT_CARD_RE_H2O.items()]
        return ctx

class ReH2OPaymentNewView(BreadCrumbsMixin, TemplateView):
    page_title = "ReH₂O"
    template_name = "payment/reh2O.html"

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        site = get_current_site(self.request)
        ss = SiteSettings.objects.get(site=site)

        ctx['title'] = _('Питна вода')
        ctx['desc'] = ss.localized_reh2o_text
        ctx['bank_attrs'] =BankTransferAttributes.objects.filter(kind=KindProject.water.value).annotate(
            order=Case(
                *[When(currency=v, then=Value(i)) for i, v in enumerate(currencies.keys())],
                default=99,
            ),
        ).order_by('order')

        ctx['credit_cards'] = [{
            'url': url,
            'currency': cur,
            'currency_sign': currencies[cur] if cur in currencies else ''
        } for cur, url in settings.PAYMENT_CARD_RE_H2O.items()]
        ctx['ctypto'] = settings.PAYMENT_CRYPTO_RE_H2O
        return ctx


class ReCityPaymentView(BreadCrumbsMixin, TemplateView):
    bc = [{'title': _("Зробити внесок")}]
    page_title = "ReCity"
    template_name = "payment/basic.html"

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['title'] = _('Дякуємо, що ви готові підтримати наш проект з відбудови житла для мешканців України!')
        ctx['credit_cards'] = [{
            'url': url,
            'currency': cur,
            'currency_sign': currencies[cur] if cur in currencies else ''
        } for cur, url in settings.PAYMENT_CARD_RE_CITY.items()]
        return ctx

class ReCityPaymentNewView(BreadCrumbsMixin, TemplateView):
    page_title = "ReCity"
    template_name = "payment/reCity.html"

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        site = get_current_site(self.request)
        ss = SiteSettings.objects.get(site=site)
        ctx['title'] = _('Відбудова')
        ctx['desc'] = ss.localized_reCity_text
        ctx['bank_attrs'] =BankTransferAttributes.objects.filter(kind=KindProject.city.value).annotate(
            order=Case(
                *[When(currency=v, then=Value(i)) for i, v in enumerate(currencies.keys())],
                default=99,
            ),
        ).order_by('order')
        ctx['credit_cards'] = [{
            'url': url,
            'currency': cur,
            'currency_sign': currencies[cur] if cur in currencies else ''
        } for cur, url in settings.PAYMENT_CARD_RE_CITY.items()]
        ctx['ctypto'] = settings.PAYMENT_CRYPTO_RE_CITY
        return ctx
