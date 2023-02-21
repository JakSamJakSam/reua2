from django.views.generic import TemplateView, FormView
from django.urls import reverse

from reua.forms.feedback import FeedbackForm
from reua.models import Partner


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


