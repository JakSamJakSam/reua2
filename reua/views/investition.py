from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView
from django.utils.translation import gettext_lazy as _

from reua.fillters import CompanyFilter, InvestitionCompanyFilter
from reua.forms.company import AddCompanyG, AddCompanyI
from reua.models import Company, CompanyCategory, InvestitionCompany

__all__ = ('ListInvestitionView', 'DetailinvestitionView', 'Addinvestition')

from reua.views.mixins import BreadCrumbsMixin


class ListInvestitionView(BreadCrumbsMixin, ListView):
    model = InvestitionCompany
    paginate_by = 10
    template_name = 'investition/investitions.html'
    bc = [{'title': _("Інвестиційна програма")}]
    page_title = _("Інвестиційна програма")

    def __init__(self, *args, **kwargs):
        self._filter = None
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        q = super().get_queryset()
        self._filter = InvestitionCompanyFilter(self.request.GET, queryset=q)
        return self._filter.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=object_list, **kwargs)
        ctx['categories'] = CompanyCategory.objects.all().annotate(companies_count=Count('investitioncompany'))
        ctx['current_category'] = self._filter.form.cleaned_data.get('category', None)
        return ctx

class Addinvestition(BreadCrumbsMixin, FormView):
    form_class = AddCompanyI
    template_name = 'investition/new_investition.html'
    bc = [        {'title': _("Інвестиційна програма"), 'url': reverse_lazy('investition-list')},
        {'title': _("Подати заявку")},

    ]
    page_title = _("Подати заявку")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        return {
            **super().get_form_kwargs(),
            'site_id': get_current_site(self.request).id
        }
    def get_success_url(self):
        return reverse_lazy('investition-list')


class DetailinvestitionView(BreadCrumbsMixin, DetailView):
    model = InvestitionCompany
    context_object_name = 'company'
    template_name = 'investition/investition.html'

    bc = [
        {'title': _("Інвестиційна програма"), 'url': reverse_lazy('investition-list')},
    ]

    def get_bc(self):
        return [*super().get_bc(), {'title': self.get_page_title()}]
    def get_page_title(self):
        return str(self.object)

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['category_companies'] = InvestitionCompany.objects.filter(category=self.object.category)
        return ctx