from enum import Enum

from adminsortable.models import SortableMixin
from django.db import models
from django.utils.translation import gettext_lazy as _, get_language

__all__ = ('Project',)

class KindProject(Enum):
    water = 1
    city = 2

kind_project_values = {
    KindProject.water.value: 'ReH2O',
    KindProject.city.value: 'ReCity',
}

currencies = {
    "UAH": "₴",
    "USD": "$",
    'EUR': "€",
    "GPB": "£",
}

for_values = {
    "for_city": _("Для міста"),
    "for": _("Для"),
}


class Project(SortableMixin, models.Model):
    kind = models.PositiveSmallIntegerField(verbose_name=_('Тип'), choices=[(k,v) for k, v in kind_project_values.items()])
    title = models.CharField(max_length=100, verbose_name=_('Назва (українською)'))
    title_en = models.CharField(max_length=100, verbose_name=_('Назва (англійською)'), blank=True)

    # short_desc = models.TextField(verbose_name=_('Короткий опис (українською)'), blank=True)
    # short_desc_en = models.TextField(verbose_name=_('Короткий опис (англійською)'), blank=True)

    desc = models.TextField(verbose_name=_('Детальний опис (українською)'), blank=True)
    desc_en = models.TextField(verbose_name=_('Детальний опис (англійською)'), blank=True)

    # target = models.DecimalField(verbose_name=_('Потрібно'), max_digits=13, decimal_places=0)
    # current = models.DecimalField(verbose_name=_('Зібрано'), max_digits=13, decimal_places=0, blank=True, default=0)
    closed = models.BooleanField(verbose_name=_('Завершено'), blank=True, default=False)

    # currency = models.CharField(max_length=3, verbose_name=_('Валюта'), choices=[(e, v) for e,v in currencies.items()], default='USD')

    order = models.PositiveSmallIntegerField(default=0, editable=False)

    image = models.ImageField(upload_to="porjects", blank=True)

    for1 = models.CharField(max_length=8, verbose_name=_('Для кого'), choices=((k,v) for k,v in for_values.items()))
    for_city = models.CharField(max_length=100, verbose_name=_('Назва населеного пункту'), blank=True)
    for_region = models.CharField(max_length=100, verbose_name=_('Назва області'), blank=True)
    for_city_en = models.CharField(max_length=100, verbose_name=_('Назва населеного пункту (англ.)'), blank=True)
    for_region_en = models.CharField(max_length=100, verbose_name=_('Назва області (англ.)'), blank=True)
    status = models.TextField(verbose_name=_('Статус'), blank=True)
    status_en = models.TextField(verbose_name=_('Статус (англ.)'), blank=True)

    @property
    def localized_title(self):
        lg = get_language()
        localized_title = getattr(self, f'title_{lg}', self.title)
        return localized_title if localized_title else self.title

    # @property
    # def localized_short_desc(self):
    #     lg = get_language()
    #     localized_short_desc = getattr(self, f'short_desc_{lg}', self.short_desc)
    #     return localized_short_desc if localized_short_desc else self.short_desc

    @property
    def localized_desc(self):
        lg = get_language()
        localized_desc = getattr(self, f'desc_{lg}', self.desc)
        return localized_desc if localized_desc else self.desc

    @property
    def localized_for1(self):
        return for_values[self.for1]

    @property
    def localized_for_city(self):
        lg = get_language()
        localized_for_city = getattr(self, f'for_city_{lg}', self.for_city)
        return localized_for_city if localized_for_city else self.for_city

    @property
    def localized_for_region(self):
        lg = get_language()
        localized_for_region = getattr(self, f'for_region_{lg}', self.for_region)
        return localized_for_region if localized_for_region else self.for_region

    @property
    def localized_status(self):
        lg = get_language()
        localized_status = getattr(self, f'status_{lg}', self.status)
        return localized_status if localized_status else self.status

    # @property
    # def currency_symbol(self):
    #     return currencies.get(self.currency, "?")

    class Meta:
        verbose_name = _("Проєкт")
        verbose_name_plural = _("Проєкти")
        ordering = ["order"]

    def __str__(self):
        return self.title


class ProjectPhoto(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name=_('Проєкт'), related_name='photos')
    photo = models.ImageField(upload_to='prj_photo', verbose_name=_('Фото'))

    class Meta:
        verbose_name = _("Фото проєкту")
        verbose_name_plural = _("Фото проєктів")

    def __str__(self):
        return f"Фото №{self.id}"

