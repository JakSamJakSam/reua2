import django_filters

from reua.models import Company, InvestitionCompany, News


class CompanyFilter(django_filters.FilterSet):
    class Meta:
        model = Company
        fields = ['category', ]

class InvestitionCompanyFilter(django_filters.FilterSet):
    class Meta:
        model = InvestitionCompany
        fields = ['category', ]

class NewsFilter(django_filters.FilterSet):
    class Meta:
        model = News
        fields = ['category', ]
