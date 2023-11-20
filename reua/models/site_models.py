from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.templatetags.static import static
from django.urls import reverse
from django.utils.translation import gettext_lazy as _, get_language
from adminsortable.models import SortableMixin

__all__ = ('TopMenu', 'FoundingDocument', 'SiteSettings', 'Staff', 'Partner', 'BankTransferAttributes', 'FeedbackMessage')

from phonenumber_field.modelfields import PhoneNumberField

from reua.models.projects import kind_project_values, currencies


class TopMenu(SortableMixin, models.Model):
    KIND_FP = 1
    KIND_BASIC = 2

    title = models.CharField(max_length=100, verbose_name=_('Назва (українською)'))
    title_en = models.CharField(max_length=100, verbose_name=_('Назва (англійською)'))
    disabled = models.BooleanField(default=False, verbose_name=_('Відключено'))
    fp = models.ForeignKey('flatpages.FlatPage', on_delete=models.RESTRICT, verbose_name=_("flat page"), null=True,
                           blank=True, default=None)
    order = models.PositiveSmallIntegerField(verbose_name=_('Номер за порядком'))
    url_name = models.CharField(max_length=100, verbose_name=_("Назва стандартної сторінки"), blank=True)
    kind = models.PositiveSmallIntegerField(verbose_name=_('Тип'), choices=(
        (KIND_FP, _("Сторінка FlatPage")),
        (KIND_BASIC, _("Стандартна сторінка")),
    ))
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, default=None, verbose_name=_('Батьківський пункт меню'), related_name='child')

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


class FoundingDocument(models.Model):
    KIND_TEXT = 'text'
    KIND_PDF = 'pdf'
    KIND_LINK = 'link'

    title = models.CharField(max_length=100, verbose_name=_('Назва (українською)'))
    title_en = models.CharField(max_length=100, verbose_name=_('Назва (англійською)'), blank=True)
    kind = models.CharField(max_length=50, verbose_name=_('Тип'), choices=(
        (KIND_TEXT, _("Текст")),
        (KIND_PDF, "PDF"),
        (KIND_LINK, _("Посилання")),
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
        return "fa-solid fa-question"

    @property
    def url(self):
        if self.kind in (self.KIND_TEXT, self.KIND_LINK):
            return self.fp.get_absolute_url()
        if self.kind in (self.KIND_PDF,):
            return reverse("pdf-item", kwargs={'pk': self.pk})
        return "#"

    @property
    def localized_title(self):
        lg = get_language()
        localized_title = getattr(self, f'title_{lg}', self.title)
        return localized_title if localized_title else self.title

    def clean(self):
        if self.kind in (self.KIND_TEXT, self.KIND_LINK) and self.fp is None:
            raise ValidationError(({'fp': _('Сторінка має бути вказана')}))
        if self.kind in (self.KIND_PDF,) and not self.file:
            raise ValidationError(({'file': _('Файл має бути вказаний')}))

    class Meta:
        verbose_name = _("Установчий документ")
        verbose_name_plural = _("Установчі документи")
        ordering = ["id"]

    def __str__(self):
        return self.title


class SiteSettings(models.Model):
    site = models.OneToOneField('sites.Site', on_delete=models.RESTRICT, verbose_name=_('Сайт'))
    company_add_code = models.CharField(max_length=20, verbose_name=_('Код додавання компанії в групу компаній'))
    invest_add_code = models.CharField(max_length=20, verbose_name=_('Код додавання компанії в інвестиції'))
    addr = models.TextField(verbose_name=_('Адреса'), blank=True)
    addr_en = models.TextField(verbose_name=_('Адреса англійською'), blank=True)
    phone = PhoneNumberField(verbose_name=_('Телефон'), region='UA', null=True, blank=True, default=None)
    phone2 = PhoneNumberField(verbose_name=_('Телефон'), region='UA', null=True, blank=True, default=None)
    email = models.EmailField(verbose_name='E-Mail', null=True, blank=True, default=None)
    lat = models.FloatField(verbose_name=_('Широта'), null=True, blank=True, default=None)
    lng = models.FloatField(verbose_name=_('Долгота'), null=True, blank=True, default=None)

    def __str__(self):
        return str(self.site)

    class Meta:
        verbose_name = _("Налаштування сайту")
        verbose_name_plural = _("Налаштування сайту")

    @property
    def localized_addr(self):
        lg = get_language()
        localized_addr = getattr(self, f'addr_{lg}', self.addr)
        return localized_addr if localized_addr else self.addr

    @property
    def coords(self):
        return {
            'lat': self.lat,
            'lng': self.lng,
            'title': 'reUA',
            'marker': static("reua/img/reua_marker2.png"),
        }


class Staff(SortableMixin, models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Ім'я та прізвище (укр)"))
    name_en = models.CharField(max_length=100, verbose_name=_("Ім'я та прізвище (англ)"), blank=True)

    position = models.CharField(max_length=100, verbose_name=_("Посада (укр)"))
    position_en = models.CharField(max_length=100, verbose_name=_("Посада (англ)"), blank=True)

    descriprion = models.TextField(verbose_name=_("Опис (укр)"), blank=True)
    descriprion_en = models.TextField(verbose_name=_("Опис (англ)"), blank=True)
    order = models.PositiveSmallIntegerField(verbose_name=_('Номер за порядком'))

    photo = models.ImageField(verbose_name=_("Фото"), upload_to='staff')

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = _("Співробітник")
        verbose_name_plural = _("Співробітники")
        ordering = ('order',)

    @property
    def localized_name(self):
        lg = get_language()
        localized_name = getattr(self, f'name_{lg}', self.name)
        return localized_name if localized_name else self.name

    @property
    def localized_position(self):
        lg = get_language()
        localized_position = getattr(self, f'position_{lg}', self.position)
        return localized_position if localized_position else self.position

    @property
    def localized_descriprion(self):
        lg = get_language()
        localized_descriprion = getattr(self, f'descriprion_{lg}', self.descriprion)
        return localized_descriprion if localized_descriprion else self.descriprion


class Partner(SortableMixin, models.Model):
    title = models.CharField(max_length=100, verbose_name=_('Назва (українською)'))
    title_en = models.CharField(max_length=100, verbose_name=_('Назва (англійською)'), blank=True)
    logo = models.ImageField(verbose_name=_('Логотип'), upload_to='partners')
    order = models.PositiveSmallIntegerField(verbose_name=_('Номер за порядком'))
    url = models.URLField(verbose_name=_('Сайт'), blank=True)

    @property
    def localized_title(self):
        lg = get_language()
        localized_title = getattr(self, f'title_{lg}', self.title)
        return localized_title if localized_title else self.title

    class Meta:
        verbose_name = _("Партнер")
        verbose_name_plural = _("Партнери")
        ordering = ["order"]

    def __str__(self):
        return self.title


class BankTransferAttributes(models.Model):
    kind = models.PositiveSmallIntegerField(verbose_name=_('Тип'),
                                            choices=[(k, v) for k, v in kind_project_values.items()])
    currency = models.CharField(max_length=3, verbose_name=_('Валюта'), choices=[(e, v) for e, v in currencies.items()])
    attr = models.TextField(verbose_name=_('Банківські реквізити (укр)'))
    attr_en = models.TextField(verbose_name=_('Банківські реквізити (англ)'), blank=True)

    @property
    def localized_attr(self):
        lg = get_language()
        localized_attr = getattr(self, f'attr_{lg}', self.attr)
        return localized_attr if localized_attr else self.attr

    def __str__(self):
        return f'{kind_project_values[self.kind]} {self.currency}'

    class Meta:
        verbose_name = _("Банківські реквізити")
        verbose_name_plural = _("Банківські реквізити")
        unique_together = (('kind', 'currency'),)



class GeneralProjectImages(SortableMixin, models.Model):
    POSITION_TOP = 1
    # POSITION_MIDDLE = 2
    POSITION_BOTTOM = 3

    kind = models.PositiveSmallIntegerField(verbose_name=_('Тип'),
                                            choices=[(k, v) for k, v in kind_project_values.items()])
    position = models.PositiveSmallIntegerField(
        verbose_name=_('Положення'),
        choices=[
            (POSITION_TOP, "Зверху"),
            # (POSITION_MIDDLE, "Середина"),
            (POSITION_BOTTOM, "Знизу"),
        ]
    )
    image = models.ImageField(upload_to='')
    order = models.PositiveSmallIntegerField(default=99, verbose_name=_('Номер за порядком'))

    def __str__(self):
        return kind_project_values[self.kind]

    class Meta:
        verbose_name = _("Зображення ReH2O та ReCity")
        verbose_name_plural = _("Зображення ReH2O та ReCity")
        ordering = ('order',)

class FeedbackMessage(models.Model):
    fio = models.CharField(max_length=100, verbose_name=_("Ім'я"))
    phone = PhoneNumberField(verbose_name=_("Номер телефону"))
    email = models.EmailField(verbose_name="E-Mail")
    message = models.TextField(verbose_name=_("Повідомлення"))
    date = models.DateTimeField(verbose_name=_("Дата та час"), auto_now_add=True)

    def __str__(self):
        return self.message

    class Meta:
        verbose_name = _("Повідомлення")
        verbose_name_plural = _("Повідомлення")
        ordering = ('date',)


class ReH2OSettings(models.Model):
    site = models.OneToOneField('sites.Site', on_delete=models.RESTRICT, verbose_name=_('Сайт'))
    video = models.ForeignKey('ReH2OVideos', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.site)

    class Meta:
        verbose_name = _("Налаштування сторінки ReH2O")
        verbose_name_plural = _("Налаштування сторінки ReH2O")


class ReH2OVideos(SortableMixin, models.Model):
    site = models.ForeignKey('sites.Site', on_delete=models.RESTRICT, verbose_name=_('Сайт'))
    title = models.CharField(max_length=100, verbose_name=_('Назва'))
    video = models.FileField(verbose_name=_('Відео'), upload_to="video")
    video_en = models.FileField(verbose_name=_('Відео (англ.)'), upload_to="video_en", null=True, blank=True, default=None)
    order = models.PositiveSmallIntegerField(default=99, verbose_name=_('Номер за порядком'))
    poster = models.ImageField(verbose_name=_('Постер'), upload_to="posters", null=True, blank=True, default=None)

    def __str__(self):
        return str(self.title)

    @property
    def localized_video(self):
        lg = get_language()
        localized_video = getattr(self, f'video_{lg}', self.video)
        return localized_video if localized_video else self.video

    class Meta:
        verbose_name = _("Відео")
        verbose_name_plural = _("Відео")
        ordering = ('order',)
