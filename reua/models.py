from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _, get_language
from phonenumber_field.modelfields import PhoneNumberField


class TopMenu(models.Model):
    KIND_FP = 1
    KIND_BASIC = 2

    title = models.CharField(max_length=100, verbose_name=_('Назва (українською)'))
    title_en = models.CharField(max_length=100, verbose_name=_('Назва (англійською)'))
    disabled = models.BooleanField(default=False, verbose_name=_('Відключено'))
    fp = models.ForeignKey('flatpages.FlatPage', on_delete=models.RESTRICT, verbose_name=_("flat page"), null=True, blank=True, default=None)
    order = models.PositiveSmallIntegerField(verbose_name=_('Номер за порядком'))
    url_name = models.CharField(max_length=100, verbose_name=_("Назва стандартної сторінки"), blank=True)
    kind = models.PositiveSmallIntegerField(verbose_name=_('Тип'), choices=(
        (KIND_FP, _("Сторінка FlatPage")),
        (KIND_BASIC, _("Стандартна сторінка")),
    ))
    def clean(self):
        if self.kind == self.KIND_FP and self.fp is None:
            raise ValidationError(({'fp': _('Сторінка має бути вказана')}))
        if self.kind == self.KIND_BASIC and not self.url_name:
                raise ValidationError(({'url_name': _('Стандартна строрінка має бути вказана')}))

    @property
    def localized_title(self):
        lg = get_language()
        localized_title = getattr(self, f'title_{lg}', self.title)
        return localized_title if localized_title else self.title

    @property
    def url(self):
        if self.kind == self.KIND_FP:
            return self.fp.get_absolute_url()
        if self.kind == self.KIND_BASIC:
            return reverse(self.url_name)
        return '#'
    class Meta:
        verbose_name = _("Пункт основного меню")
        verbose_name_plural = _("Пункти основного меню")
        ordering = ["order"]

    def __str__(self):
        return self.title


class Partner(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('Назва (українською)'))
    title_en = models.CharField(max_length=100, verbose_name=_('Назва (англійською)'), blank=True)
    logo = models.ImageField(verbose_name=_('Логотип'), upload_to='partners')

    @property
    def localized_title(self):
        lg = get_language()
        localized_title = getattr(self, f'title_{lg}', self.title)
        return localized_title if localized_title else self.title

    class Meta:
        verbose_name = _("Партнер")
        verbose_name_plural = _("Партнери")
        ordering = ["id"]

    def __str__(self):
        return self.title


class FoundingDocument(models.Model):
    KIND_TEXT = 'text'
    KIND_PDF = 'pdf'
    KIND_LINK = 'link'

    title = models.CharField(max_length=100, verbose_name=_('Назва (українською)'))
    title_en = models.CharField(max_length=100, verbose_name=_('Назва (англійською)'), blank=True)
    kind = models.CharField(max_length=50, verbose_name=_('Тип'), choices=(
        (KIND_TEXT,_("Текст")),
        (KIND_PDF,"PDF"),
        (KIND_LINK,_("Посилання")),
    ))
    fp = models.ForeignKey('flatpages.FlatPage', on_delete=models.RESTRICT,
                           verbose_name=_("flat page"), null=True, blank=True, default=None)
    file = models.FileField(verbose_name=_("Файл (pdf)"), upload_to="files", null=True, blank=True, default=None,
                            validators=[FileExtensionValidator(allowed_extensions=('pdf',))])

    @property
    def awesome_icon(self):
        if self.kind == self.KIND_TEXT:
            return "fa-solid fa-file-invoice"
        if self.kind == self.KIND_PDF:
            return "fa-solid fa-file-pdf"
        if self.kind == self.KIND_LINK:
            return "fa-solid fa-link"
        return  "fa-solid fa-question"

    @property
    def url(self):
        if self.kind in (self.KIND_TEXT, self.KIND_LINK):
            return self.fp.get_absolute_url()
        if self.kind in (self.KIND_PDF, ):
            return self.file.url
        return "#"

    @property
    def localized_title(self):
        lg = get_language()
        localized_title = getattr(self, f'title_{lg}', self.title)
        return localized_title if localized_title else self.title

    def clean(self):
        if self.kind in (self.KIND_TEXT, self.KIND_LINK) and self.fp is None:
            raise ValidationError(({'fp': _('Сторінка має бути вказана')}))
        if self.kind in (self.KIND_PDF, ) and not self.file:
            raise ValidationError(({'file': _('Файл має бути вказаний')}))

    class Meta:
        verbose_name = _("Установчий документ")
        verbose_name_plural = _("Установчі документи")
        ordering = ["id"]

    def __str__(self):
        return self.title

class CompanyCategory(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('Назва (українською)'))
    title_en = models.CharField(max_length=100, verbose_name=_('Назва (англійською)'), null=True, blank=True, default=None)

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


class AbstractCompany(models.Model):
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
    repr_status= models.PositiveSmallIntegerField(verbose_name=_('Статус представника'), choices=(
        (REPR_STATUS_OWNER, _('Засновник')),
        (REPR_STATUS_DIR, _('Директор')),
        (REPR_STATUS_BOSS, _('Керівник')),
        (REPR_STATUS_MGR, _('Менеджер')),
    ))
    repr_phone = PhoneNumberField(verbose_name=_('Телефон представника'), region='UA', null=True, blank=True, default=None)
    repr_email = models.EmailField(verbose_name=_('E-Mail представника'), null=True, blank=True, default=None)

    def __str__(self):
        return self.name
    class Meta:
        abstract=True

class Company(AbstractCompany):
    class Meta:
        verbose_name = _("Компанія")
        verbose_name_plural = _("Компанії")
        ordering = ["id"]


class InvestitionCompany(AbstractCompany):
    class Meta:
        verbose_name = _("Компанія (інвестиція)")
        verbose_name_plural = _("Компанії (інвестиція)")
        ordering = ["id"]

class SiteSettings(models.Model):
    site = models.OneToOneField('sites.Site', on_delete=models.RESTRICT, verbose_name=_('Сайт'))
    company_add_code = models.CharField(max_length=20, verbose_name=_('Код додавання компанії в групу компаній'))
    invest_add_code = models.CharField(max_length=20, verbose_name=_('Код додавання компанії в інвестиції'))

    def __str__(self):
        return str(self.site)

    class Meta:
        verbose_name = _("Налаштування сайту")
        verbose_name_plural = _("Налаштування сайту")
