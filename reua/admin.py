from adminsortable.admin import SortableAdmin
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_summernote.admin import SummernoteModelAdmin, SummernoteModelAdminMixin

from reua.forms.admin_forms import TopMenuAdminForm
from reua.models import TopMenu, Partner, FoundingDocument, CompanyCategory, Company, SiteSettings, InvestitionCompany, \
    Staff, WaterStation
from reua.models.compaies import Label
from reua.models.projects import Project


@admin.register(TopMenu)
class TopMenuAdmin(SortableAdmin):
    form = TopMenuAdminForm


@admin.register(Partner)
class TopMenuAdmin(SortableAdmin):
    pass


admin.site.register(FoundingDocument, admin.ModelAdmin)

admin.site.register(CompanyCategory, admin.ModelAdmin)


@admin.register(InvestitionCompany)
class InvestitionCompanyAdmin(SortableAdmin):
    fieldsets = (
        (_('Адмінистрування'), {
            'classes': ('collapse',),
            'fields': ('labels', ),
        }),
        (_('Реквізити компанії'), {
            'fields': ('name', 'category', 'logotype', 'descr', 'city', 'addr', 'phone', 'email', 'site')
        }),
        (_('Представник компанії'), {
            # 'classes': ('extrapretty1',),#wide, extrapretty, collapse
            'fields': ('repr_fio', 'repr_status', 'repr_phone', 'repr_email'),
        }),
    )


@admin.register(Company)
class CompanyAdmin(SortableAdmin):
    fieldsets = (
        (_('Адмінистрування'), {
            'classes': ('collapse',),
            'fields': ('labels', ),
        }),
        (_('Реквізити компанії'), {
            'fields': ('name', 'category', 'logotype', 'descr', 'city', 'addr', 'phone', 'email', 'site')
        }),
        (_('Представник компанії'), {
            # 'classes': ('extrapretty1',),#wide, extrapretty, collapse
            'fields': ('repr_fio', 'repr_status', 'repr_phone', 'repr_email'),
        }),
    )


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Адреса'), {
            # 'classes': ('collapse',),
            'fields': ('addr', 'addr_en', 'phone', 'email', 'lat', 'lng'),
        }),
        (_('Коди'), {
            'classes': ('collapse',),
            'fields': ('company_add_code', 'invest_add_code'),
        }),
    )

@admin.register(Staff)
class StaffAdmin(SummernoteModelAdmin):
    summernote_fields = ('descriprion', 'descriprion_en')


@admin.register(Label)
class LabelAdmin(SortableAdmin):
    pass

@admin.register(WaterStation)
class LabelAdmin(SortableAdmin):
    pass


@admin.register(Project)
class ProjectAdmin(SummernoteModelAdminMixin, SortableAdmin):
    list_display = ('title', 'target', 'current', 'closed')
    summernote_fields = ('desc', 'desc_en')

