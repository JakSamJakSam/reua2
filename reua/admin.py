from adminsortable.admin import SortableAdmin
from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import gettext_lazy as _
from django_summernote.admin import SummernoteModelAdmin, SummernoteModelAdminMixin

from reua.forms.admin_forms import TopMenuAdminForm
from reua.models import *
from reua.models.projects import ProjectPhoto
from reua.models.site_models import GeneralProjectImages, FeedbackMessage, ReH2OSettings, ReH2OVideos
from reua.models.waters import ActivePoints


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
    search_fields = ('name', 'name_en')
    list_filter = ('category',)
    fieldsets = (
        (_('Адмінистрування'), {
            'classes': ('collapse',),
            'fields': ('labels', ),
        }),
        (_('Реквізити компанії'), {
            'fields': ('name', 'category', 'logotype', 'city', 'addr', 'phone', 'email', 'site')
        }),
        (_('Реквізити компанії англ.'), {
            'fields': ('name_en', 'city_en', 'addr_en', 'descr_en')
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
    search_fields = ('name', 'name_en')
    list_filter = ('category',)
    fieldsets = (
        (_('Адмінистрування'), {
            'classes': ('collapse',),
            'fields': ('labels', ),
        }),
        (_('Реквізити компанії'), {
            'fields': ('name', 'category', 'logotype', 'descr', 'city', 'addr', 'phone', 'email', 'site')
        }),
        (_('Реквізити компанії англ.'), {
            'fields': ('name_en', 'city_en', 'addr_en', 'descr_en')
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
            'fields': ('addr', 'addr_en', 'phone', 'phone2', 'email', 'lat', 'lng'),
        }),
        (_('Коди'), {
            'classes': ('collapse',),
            'fields': ('company_add_code', 'invest_add_code'),
        }),
    )

@admin.register(Staff)
class StaffAdmin(SummernoteModelAdminMixin, SortableAdmin):
    summernote_fields = ('descriprion', 'descriprion_en')


@admin.register(Label)
class LabelAdmin(SortableAdmin):
    pass

@admin.register(WaterStation)
class LabelAdmin(SortableAdmin):
    pass

class ProjectPhotoInline(admin.StackedInline):
    model = ProjectPhoto

@admin.register(Project)
class ProjectAdmin(SummernoteModelAdminMixin, SortableAdmin):
    inlines = [
        ProjectPhotoInline,
    ]
    list_display = ('title', 'target', 'current', 'closed')
    summernote_fields = ('desc', 'desc_en')
    fieldsets = [
        ('Назва та опис', {
            'fields': [
                'kind', 'title','short_desc', 'desc', 'image'
            ],
        }),
        ('Назва та опис (англ)', {
            'fields': [
                'title_en','short_desc_en', 'desc_en'
            ],
        }),
        ('Ціль', {
            'fields': [
                'currency', 'target', 'current', 'closed'
            ],
        }),
        ('Для кого', {
            'fields': [
                'for1', 'for_city', 'for_region'
            ],
        }),
        ('Для кого (агнл)', {
            'fields': [
                'for_city_en', 'for_region_en'
            ],
        }),
        ('Статсу', {
            'fields': [
                'status', 'status_en'
            ],
        }),
    ]


admin.site.register(NewsCategory, admin.ModelAdmin)


class NewsImagesInline(admin.TabularInline):
    model = NewsImages

@admin.register(News)
class NewsAdmin(SummernoteModelAdmin):
    list_display = ('title', 'date', 'category', 'enabled')
    summernote_fields = ('body', 'body_en')
    date_hierarchy = 'date'
    list_filter = ('category', )
    inlines = [NewsImagesInline,]

    actions = ["make_enabled", "make_disabled"]

    @admin.action(description=_("Опублікувати обрані новини"))
    def make_enabled(self, request, queryset):
        queryset.update(enabled=True)

    @admin.action(description=_("Приховати обрані новини"))
    def make_disabled(self, request, queryset):
        queryset.update(enabled=False)


class NewFlatPageAdmin(SummernoteModelAdminMixin, FlatPageAdmin):
    summernote_fields = ('content', )

# Re-register FlatPageAdmin
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, NewFlatPageAdmin)

@admin.register(BankTransferAttributes)
class BankTransferAttributesAdmin(SummernoteModelAdmin):
    list_display = ('kind', 'currency',)
    summernote_fields = ('attr', 'attr_en')
    list_filter = ('kind', 'currency' )


@admin.register(GeneralProjectImages)
class ProjectAdmin(SortableAdmin):
    pass


@admin.register(FeedbackMessage)
class FeedbackMessageAdmin(admin.ModelAdmin):
    search_fields = ('message', 'fio', 'phone', 'email')
    date_hierarchy = ('date')
    list_display = ('fio', 'phone', 'email', 'message')

@admin.register(ReH2OSettings)
class ReH2OSettingsAdmin(admin.ModelAdmin):
    pass


@admin.register(ReH2OVideos)
class ReH2OVideosAdmin(SortableAdmin):
    pass


@admin.register(ActivePoints)
class ActivePointsAdmin(admin.ModelAdmin):
    pass
