from adminsortable.admin import SortableAdmin
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_summernote.admin import SummernoteModelAdmin, SummernoteModelAdminMixin

from reua.forms.admin_forms import TopMenuAdminForm
from reua.models import *

@admin.register(TopMenu)
class TopMenuAdmin(SortableAdmin):
    form = TopMenuAdminForm


@admin.register(Partner)
class TopMenuAdmin(SortableAdmin):
    pass


admin.site.register(FoundingDocument, admin.ModelAdmin)

@admin.register(CompanyCategory)
class CompanyCategoryAdmin(SortableAdmin):
    pass

@admin.register(InvestitionCategory)
class InvestitionCategoryAdmin(SortableAdmin):
    pass


@admin.register(InvestitionCompany)
class InvestitionCompanyAdmin(SortableAdmin):
    fieldsets = (
        (_('Адмінистрування'), {
            'classes': ('collapse',),
            'fields': ('labels', ),
        }),
        (_('Реквізити компанії'), {
            'fields': ('name', 'category', 'logotype', 'city', 'addr', 'phone', 'email', 'site')
        }),
        (_('Реквізити інвестиції'), {
            'fields': ('descr', 'is_active', 'target_amount', 'turnover_1', 'turnover_2', 'turnover_3', 'quant_of_persons')
        }),
        (_('Файли'), {
            'fields': ('business_plan', 'feasibility_study', )
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


admin.site.register(NewsCategory, admin.ModelAdmin)


class NewsImagesInline(admin.TabularInline):
    model = NewsImages

@admin.register(News)
class NewsAdmin(SummernoteModelAdmin):
    list_display = ('title', 'date', 'category')
    summernote_fields = ('body', 'body_en')
    date_hierarchy = 'date'
    list_filter = ('category', )
    inlines = [NewsImagesInline,]

