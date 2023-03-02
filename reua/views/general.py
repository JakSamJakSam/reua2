from django.urls import reverse
from django.views.generic import TemplateView, FormView
from django.utils.translation import gettext_lazy as _

from reua.forms.feedback import FeedbackForm
from reua.models import Partner, Staff

__all__ = ('IndexView', 'FeedbackFormView', "AboutView", "WaterView", "RebuildView")

from reua.views.mixins import BreadCrumbsMixin


class IndexView(TemplateView):
    template_name = 'index/index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['partners'] = Partner.objects.all()
        return ctx

class FeedbackFormView(FormView):
    form_class = FeedbackForm
    template_name = 'feedback.html'

    def form_valid(self, form):
        # TODO: send message to admins
        return super().form_valid(form)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        result=super().get_context_data(**kwargs)
        result['feedback_form']=result['form']
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


class RebuildView(BreadCrumbsMixin, TemplateView):
    bc = [{'title': _("Відбудова")}]
    page_title = _("Відбудова житла")
    template_name = "pages/rebuild.html"

