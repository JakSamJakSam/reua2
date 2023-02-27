from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView
from django.utils.translation import gettext_lazy as _

from reua.fillters import CompanyFilter
from reua.forms.company import AddCompanyG
from reua.models import Company, CompanyCategory

__all__ = ('ListCompanyView', 'DetailCompanyView', 'AddCompany')

from reua.views.mixins import BreadCrumbsMixin


class ListCompanyView(BreadCrumbsMixin, ListView):
    model = Company
    paginate_by = 10
    template_name = 'company/companies.html'
    bc = [{'title': _("Група компаній")}]
    page_title = _("Група компаній")

    def __init__(self, *args, **kwargs):
        self._filter = None
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        q = super().get_queryset()
        # for i in range(0,10):
        #     q = q.union(q, all=True)
        self._filter = CompanyFilter(self.request.GET, queryset=q)
        return self._filter.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=object_list, **kwargs)
        ctx['categories'] = CompanyCategory.objects.all().annotate(companies_count=Count('company'))
        ctx['current_category'] = self._filter.form.cleaned_data.get('category', None)
        return ctx

class AddCompany(BreadCrumbsMixin, FormView):
    form_class = AddCompanyG
    template_name = 'company/new_company.html'
    bc = [        {'title': _("Група компаній"), 'url': reverse_lazy('company-list')},
        {'title': _("Подати заявку")},

    ]
    page_title = _("Подати заявку")

    def form_valid(self, form):
        instance = form.instance
        instance.save()
        return super().form_valid(form)
    def get_form_kwargs(self):
        return {
            **super().get_form_kwargs(),
            'site_id': get_current_site(self.request).id
        }
    def get_success_url(self):
        return reverse_lazy('company-list')


class DetailCompanyView(BreadCrumbsMixin, DetailView):
    model = Company
    context_object_name = 'company'
    template_name = 'company/company.html'

    bc = [
        {'title': _("Група компаній"), 'url': reverse_lazy('company-list')},
    ]

    def get_bc(self):
        return [*super().get_bc(), {'title': self.get_page_title()}]
    def get_page_title(self):
        return str(self.object)

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['category_companies'] = Company.objects.filter(category=self.object.category)
        return ctx