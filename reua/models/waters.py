from adminsortable.models import SortableMixin
from django.db import models
from django.utils.translation import gettext_lazy as _, get_language
from reua.enums import UaRegions

__all__ = ('WaterStation', 'MapPoint')

class MapPoint(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('Назва (українською)'))
    title_en = models.CharField(max_length=100, verbose_name=_('Назва (англійською)'), blank=True)

    region = models.CharField(max_length=16, verbose_name=_('Регіон'), choices=UaRegions)
    lon = models.FloatField(verbose_name=_("Довгота"))
    lat = models.FloatField(verbose_name=_("Широта"))

    @property
    def localized_title(self):
        lg = get_language()
        localized_title = getattr(self, f'title_{lg}', self.title)
        return localized_title if localized_title else self.title

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Крапка на мапі")
        verbose_name_plural = _("Крапки на мапі")


class WaterStation(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('Назва (українською)'))
    point = models.ForeignKey(MapPoint, on_delete=models.RESTRICT, verbose_name=_("Крапка на мапі"), related_name='stations', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Установка очищення води")
        verbose_name_plural = _("Установки очищення води")



