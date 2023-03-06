from enum import Enum

from adminsortable.models import SortableMixin
from django.db import models
from django.utils.translation import gettext_lazy as _, get_language

__all__ = ('Project',)

class KindProject(Enum):
    water = 1
    city = 2

kind_project_values = (
    (KindProject.water.value, 'ReH2O'),
    (KindProject.city.value, 'ReCity'),
)

currencies = {
    'EUR': "€",
    "USD": "$",
    "UAH": "₴",
}


class Project(SortableMixin, models.Model):
    kind = models.PositiveSmallIntegerField(verbose_name=_('Тип'), choices=kind_project_values)
    title = models.CharField(max_length=100, verbose_name=_('Назва (українською)'))
    title_en = models.CharField(max_length=100, verbose_name=_('Назва (англійською)'), blank=True)

    short_desc = models.TextField(verbose_name=_('Короткий опис (українською)'), blank=True)
    short_desc_en = models.TextField(verbose_name=_('Короткий опис (англійською)'), blank=True)

    desc = models.TextField(verbose_name=_('Детальний опис (українською)'), blank=True)
    desc_en = models.TextField(verbose_name=_('Детальний опис (англійською)'), blank=True)

    target = models.DecimalField(verbose_name=_('Потрібно'), max_digits=13, decimal_places=0)
    current = models.DecimalField(verbose_name=_('Зібрано'), max_digits=13, decimal_places=0, blank=True, default=0)
    closed = models.BooleanField(verbose_name=_('Завершено'), blank=True, default=False)

    currency = models.CharField(max_length=3, verbose_name=_('Валюта'), choices=[(e, v) for e,v in currencies.items()], default='USD')

    order = models.PositiveSmallIntegerField(default=0, editable=False)

    image = models.ImageField(upload_to="porjects", blank=True)

    @property
    def localized_title(self):
        lg = get_language()
        localized_title = getattr(self, f'title_{lg}', self.title)
        return localized_title if localized_title else self.title

    @property
    def localized_short_desc(self):
        lg = get_language()
        localized_short_desc = getattr(self, f'short_desc_{lg}', self.short_desc)
        return localized_short_desc if localized_short_desc else self.short_desc

    @property
    def localized_desc(self):
        lg = get_language()
        localized_desc = getattr(self, f'desc_{lg}', self.desc)
        return localized_desc if localized_desc else self.desc

    @property
    def currency_symbol(self):
        return currencies.get(self.currency, "?")

    class Meta:
        verbose_name = _("Проєкт")
        verbose_name_plural = _("Проєкти")
        ordering = ["order"]

    def __str__(self):
        return self.title

