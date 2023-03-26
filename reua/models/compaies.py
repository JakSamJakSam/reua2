from adminsortable.models import SortableMixin
from django.utils.translation import gettext_lazy as _, get_language
from django.db import models

__all__ = ('CompanyCategory', 'Company', 'InvestitionCompany', 'InvestitionCategory', 'Label')

from phonenumber_field.modelfields import PhoneNumberField


class Label(SortableMixin, models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Назва'))

    html_code = models.TextField(verbose_name=_('Код HTML (укр)'))
    html_code_en = models.TextField(verbose_name=_('Код HTML (aнгл)'), blank=True)

    order = models.PositiveSmallIntegerField(verbose_name=_('Номер за порядком'))
    def __str__(self):
        return self.name

    @property
    def localized_html_code(self):
        lg = get_language()
        localized_html_code = getattr(self, f'html_code_{lg}', self.html_code)
        return localized_html_code if localized_html_code else self.html_code

    class Meta:
        verbose_name = _("Мітка  компанії")
        verbose_name_plural = _("Мітки компаній")
        ordering = ["order"]


class AbstractCategory(SortableMixin, models.Model):
    title = models.CharField(max_length=100, verbose_name=_('Назва (українською)'))
    title_en = models.CharField(max_length=100, verbose_name=_('Назва (англійською)'), null=True, blank=True,
                                default=None)
    order = models.PositiveSmallIntegerField(blank=True,
                                default=999999)
    def __str__(self):
        return self.localized_title

    @property
    def localized_title(self):
        lg = get_language()
        localized_title = getattr(self, f'title_{lg}', self.title)
        return localized_title if localized_title else self.title

    class Meta:
        abstract = True
class CompanyCategory(AbstractCategory):
    class Meta:
        verbose_name = _("Категорія компаній")
        verbose_name_plural = _("Категорії компаній")
        ordering = ["order"]

class InvestitionCategory(AbstractCategory):
    class Meta:
        verbose_name = _("Категорія інвестицый")
        verbose_name_plural = _("Категорії інвестицый")
        ordering = ["order"]


class AbstractCompany(SortableMixin, models.Model):
    REPR_STATUS_OWNER = 1
    REPR_STATUS_DIR = 2
    REPR_STATUS_BOSS = 3
    REPR_STATUS_MGR = 4

    name = models.CharField(max_length=200, verbose_name=_('Назва компанії'))
    name_en = models.CharField(max_length=200, verbose_name=_('Назва компанії (англ.)'), blank=True, default='')
    logotype = models.ImageField(upload_to='company', verbose_name=_('Логотип'), null=True, blank=True, default=None)
    descr = models.TextField(verbose_name=_('Опис'), blank=True, default='')
    descr_en = models.TextField(verbose_name=_('Опис (англ.)'), blank=True, default='')
    city = models.CharField(max_length=100, verbose_name=_('Місто'), null=True, blank=True, default=None)
    city_en = models.CharField(max_length=100, verbose_name=_('Місто (англ.)'), null=True, blank=True, default=None)
    addr = models.TextField(max_length=100, verbose_name=_('Адреса'), null=True, blank=True, default=None)
    addr_en = models.TextField(max_length=100, verbose_name=_('Адреса (англ.)'), null=True, blank=True, default=None)
    phone = PhoneNumberField(verbose_name=_('Телефон'), region='UA', null=True, blank=True, default=None)
    email = models.EmailField(verbose_name='E-Mail', null=True, blank=True, default=None)
    site = models.URLField(verbose_name=_('Сайт'), null=True, blank=True, default=None)
    repr_fio = models.CharField(max_length=200, verbose_name=_('ПІБ'))
    repr_status = models.PositiveSmallIntegerField(verbose_name=_('Статус представника'), choices=(
        (REPR_STATUS_OWNER, _('Засновник')),
        (REPR_STATUS_DIR, _('Директор')),
        (REPR_STATUS_BOSS, _('Керівник')),
        (REPR_STATUS_MGR, _('Менеджер')),
    ))
    repr_phone = PhoneNumberField(verbose_name=_('Телефон представника'), region='UA', null=True, blank=True,
                                  default=None)
    repr_email = models.EmailField(verbose_name=_('E-Mail представника'), null=True, blank=True, default=None)
    order = models.PositiveSmallIntegerField(verbose_name=_('Номер за порядком'))
    labels = models.ManyToManyField(Label, verbose_name=_('Мітки'), blank=True)

    @property
    def localized_name(self):
        lg = get_language()
        localized_name = getattr(self, f'name_{lg}', self.name)
        return localized_name if localized_name else self.name

    @property
    def localized_descr(self):
        lg = get_language()
        localized_descr = getattr(self, f'descr_{lg}', self.descr)
        return localized_descr if localized_descr else self.descr

    @property
    def localized_city(self):
        lg = get_language()
        localized_city = getattr(self, f'city_{lg}', self.city)
        return localized_city if localized_city else self.city

    @property
    def localized_addr(self):
        lg = get_language()
        localized_addr = getattr(self, f'addr_{lg}', self.addr)
        return localized_addr if localized_addr else self.addr

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Company(AbstractCompany):
    category = models.ForeignKey(CompanyCategory, on_delete=models.PROTECT, verbose_name=_('Категорія'))
    class Meta:
        verbose_name = _("Компанія")
        verbose_name_plural = _("Компанії")
        ordering = ["order"]


class InvestitionCompany(AbstractCompany):
    category = models.ForeignKey(InvestitionCategory, on_delete=models.PROTECT, verbose_name=_('Категорія'))
    descr = models.TextField(verbose_name=_('Короткий опис проєкту'), blank=True, default='')
    is_active = models.BooleanField(verbose_name=_('Діючий бізнес'), blank=True, default=False)
    business_plan = models.FileField(verbose_name=_('Бізнес план'), blank=True, help_text=_('Якщо є'), upload_to='documents/plan')
    feasibility_study = models.FileField(verbose_name=_('Техніко-економічне обґрунтування'), blank=True, help_text=_('Якщо є'), upload_to='documents/teo')
    target_amount = models.DecimalField(max_digits=13, decimal_places=0, verbose_name=_('Сума необхідних інвестицій, USD'))
    turnover_1 = models.DecimalField(
        max_digits=13, decimal_places=0, verbose_name=_('Оборот за попередній рік, грн'),
        blank=True, null=True, default=None
    )
    turnover_2 = models.DecimalField(
        max_digits=13, decimal_places=0, verbose_name=_('Оборот за рік - 2, грн'),
        blank=True, null=True, default=None
    )
    turnover_3 = models.DecimalField(
        max_digits=13, decimal_places=0, verbose_name=_('Оборот за рік - 3, грн'),
        blank=True, null=True, default=None
    )
    registration_date = models.DateTimeField(editable=False, auto_now_add=True)
    quant_of_persons = models.PositiveSmallIntegerField(
        verbose_name=_('Кількість співробітників'),
        help_text=_('Кількість співробітників що залучені, або планується залучити')
    )

    class Meta:
        verbose_name = _("Компанія (інвестиція)")
        verbose_name_plural = _("Компанії (інвестиція)")
        ordering = ["order"]
