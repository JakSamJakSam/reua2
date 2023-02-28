from adminsortable.admin import SortableAdmin
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_summernote.admin import SummernoteModelAdmin

from reua.forms.admin_forms import TopMenuAdminForm
from reua.models import TopMenu, Partner, FoundingDocument, CompanyCategory, Company, SiteSettings, InvestitionCompany, \
    Staff


@admin.register(TopMenu)
class TopMenuAdmin(SortableAdmin):
    form = TopMenuAdminForm

@admin.register(Partner)
class TopMenuAdmin(SortableAdmin):
    pass

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

@admin.register(Staff)
class StaffAdmin(SummernoteModelAdmin):
    summernote_fields = ('descriprion', 'descriprion_en')

