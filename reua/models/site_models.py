from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _, get_language
from adminsortable.models import SortableMixin

__all__ = ('TopMenu', 'FoundingDocument', 'SiteSettings', 'Staff', 'Partner')


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

    def __str__(self):
        return str(self.site)

    class Meta:
        verbose_name = _("Налаштування сайту")
        verbose_name_plural = _("Налаштування сайту")


class Staff(SortableMixin, models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Ім'я та прізвище (укр)"))
    name_en = models.CharField(max_length=100, verbose_name=_("Ім'я та прізвище (англ)"), blank=True)

    position = models.CharField(max_length=100, verbose_name=_("Посада (укр)"))
    position_en = models.CharField(max_length=100, verbose_name=_("Посада (англ)"), blank=True)

    descriprion = models.TextField(verbose_name="Опис (укр)", blank=True)
    descriprion_en = models.TextField(verbose_name="Опис (англ)", blank=True)
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
