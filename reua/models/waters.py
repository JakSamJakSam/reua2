from adminsortable.models import SortableMixin
from django.db import models
from django.utils.translation import gettext_lazy as _, get_language

__all__ = ('WaterStation',)


class WaterStation(SortableMixin, models.Model):
    title = models.CharField(max_length=100, verbose_name=_('Назва (українською)'))
    title_en = models.CharField(max_length=100, verbose_name=_('Назва (англійською)'), blank=True)

    lat = models.FloatField(verbose_name=_('Широта'))
    lng = models.FloatField(verbose_name=_('Долгота'))

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


point_choices = {
    **{f'p{n}': f'Київська обл {n}' for n in range(1, 28)},
    **{f'p{n}': f'Чернігіська обл {n}' for n in range(28, 58)},
    **{f'p{n}': f'Сумська обл {n}' for n in range(58, 76)},
    **{f'p{n}': f'Полтавська обл {n}' for n in range(76, 102)},
    **{f'p{n}': f'Кіровоградська обл {n}' for n in range(102, 123)},
    **{f'p{n}': f'Харківьска обл {n}' for n in range(123, 144)},
    **{f'p{n}': f'Дніпропетрівська обл {n}' for n in range(144, 178)},
    **{f'p{n}': f'Микалоївська обл {n}' for n in range(178, 198)},
    **{f'p{n}': f'Одеська обл {n}' for n in range(198, 230)},
    **{f'p{n}': f'Херсонська обл {n}' for n in range(230, 245)},
    **{f'p{n}': f'Запорізька обл {n}' for n in range(245, 264)},
}


class ActivePoints(models.Model):
    point = models.CharField(max_length=4, verbose_name=_('Точка'), choices=((k, v) for k, v in point_choices.items()))
    active = models.BooleanField(default=True, verbose_name=_('Активно'))
    description = models.TextField(blank=True, verbose_name=_('Опис'))

    def __str__(self):
        return point_choices[self.point]

    class Meta:
        verbose_name = _("Точка на мапі")
        verbose_name_plural = _("Точки на мапі")
