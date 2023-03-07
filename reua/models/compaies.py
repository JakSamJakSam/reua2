from adminsortable.models import SortableMixin
from django.utils.translation import gettext_lazy as _, get_language
from django.db import models

__all__ = ('CompanyCategory', 'Company', 'InvestitionCompany')

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


class CompanyCategory(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('Назва (українською)'))
    title_en = models.CharField(max_length=100, verbose_name=_('Назва (англійською)'), null=True, blank=True,
                                default=None)

    def __str__(self):
        return self.title

    @property
    def localized_title(self):
        lg = get_language()
        localized_title = getattr(self, f'title_{lg}', self.title)
        return localized_title if localized_title else self.title

    class Meta:
        verbose_name = _("Категорія компаній")
        verbose_name_plural = _("Категорії компаній")
        ordering = ["id"]


class AbstractCompany(SortableMixin, models.Model):
    REPR_STATUS_OWNER = 1
    REPR_STATUS_DIR = 2
    REPR_STATUS_BOSS = 3
    REPR_STATUS_MGR = 4

    name = models.CharField(max_length=200, verbose_name=_('Назва компанії'))
    logotype = models.ImageField(upload_to='company', verbose_name=_('Логотип'), null=True, blank=True, default=None)
    descr = models.TextField(verbose_name=('Опис'), blank=True, default='')
    city = models.CharField(max_length=100, verbose_name=_('Місто'), null=True, blank=True, default=None)
    addr = models.TextField(max_length=100, verbose_name=_('Адреса'), null=True, blank=True, default=None)
    phone = PhoneNumberField(verbose_name=_('Телефон'), region='UA', null=True, blank=True, default=None)
    email = models.EmailField(verbose_name='E-Mail', null=True, blank=True, default=None)
    site = models.URLField(verbose_name=_('Сайт'), null=True, blank=True, default=None)
    category = models.ForeignKey(CompanyCategory, on_delete=models.PROTECT, verbose_name=_('Категорія'))
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

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Company(AbstractCompany):
    class Meta:
        verbose_name = _("Компанія")
        verbose_name_plural = _("Компанії")
        ordering = ["order"]


class InvestitionCompany(AbstractCompany):
    class Meta:
        verbose_name = _("Компанія (інвестиція)")
        verbose_name_plural = _("Компанії (інвестиція)")
        ordering = ["order"]
