from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _, get_language


class TopMenu(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('Назва (українською)'))
    title_en = models.CharField(max_length=100, verbose_name=_('Назва (англійською)'))
    disabled = models.BooleanField(default=False, verbose_name=_('Відключено'))
    fp = models.ForeignKey('flatpages.FlatPage', on_delete=models.RESTRICT, verbose_name=_("flat page"))
    order = models.PositiveSmallIntegerField(verbose_name=_('Номер за порядком'))

    @property
    def localized_title(self):
        lg = get_language()
        localized_title = getattr(self, f'title_{lg}', self.title)
        return localized_title if localized_title else self.title

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
