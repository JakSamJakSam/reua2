from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from reua.forms.admin_forms import TopMenuAdminForm
from reua.models import TopMenu, Partner, FoundingDocument, CompanyCategory, Company, SiteSettings, InvestitionCompany


@admin.register(TopMenu)
class TopMenuAdmin(admin.ModelAdmin):
    form = TopMenuAdminForm

admin.site.register(Partner, admin.ModelAdmin)

admin.site.register(FoundingDocument, admin.ModelAdmin)

admin.site.register(CompanyCategory, admin.ModelAdmin)

admin.site.register(InvestitionCompany, admin.ModelAdmin)

@admin.register(Company)
class TopMenuAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Реквізити компанії'), {
            'fields': ('name', 'category', 'logotype', 'descr', 'city', 'addr', 'phone', 'email',  'site')
        }),
        (_('Представник компанії'), {
            # 'classes': ('extrapretty1',),#wide, extrapretty, collapse
            'fields': ('repr_fio', 'repr_status', 'repr_phone', 'repr_email'),
        }),
    )

admin.site.register(SiteSettings, admin.ModelAdmin)
