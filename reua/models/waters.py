from adminsortable.models import SortableMixin
from django.db import models
from django.utils.translation import gettext_lazy as _, get_language

__all__= ('WaterStation',)

class WaterStation(SortableMixin, models.Model):
    title = models.CharField(max_length=100, verbose_name=_('Назва (українською)'))
    title_en = models.CharField(max_length=100, verbose_name=_('Назва (англійською)'), blank=True)

    lat=models.FloatField(verbose_name=_('Широта'))
    lng=models.FloatField(verbose_name=_('Долгота'))

    desc = models.TextField(verbose_name=_('Опис (українською)'), blank=True)
    desc_en = models.TextField(verbose_name=_('Опис (англійською)'), blank=True)

    order = models.PositiveSmallIntegerField(verbose_name=_('Номер за порядком'))

    @property
    def localized_title(self):
        lg = get_language()
        localized_title = getattr(self, f'title_{lg}', self.title)
        return localized_title if localized_title else self.title

    @property
    def localized_desc(self):
        lg = get_language()
        localized_desc = getattr(self, f'title_{lg}', self.desc)
        return localized_desc if localized_desc else self.desc

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = _("Установка очищення води")
        verbose_name_plural = _("Установки очищення води")
        ordering = ["order"]
