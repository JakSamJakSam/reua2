from django.urls import reverse
from django.utils.translation import gettext_lazy as _

class BreadCrumbsMixin:
    bc = []
    page_title = ''
    def get_bc(self):
        return self.bc
    
    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['breadcrumbs'] = self.get_bc()
        ctx['page_title'] = self.get_page_title()
        return ctx

    def get_page_title(self):
        return self.page_title