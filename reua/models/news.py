from django.db import models
from django.utils.translation import gettext_lazy as _, get_language

__all__ = ('NewsCategory', 'News', 'NewsImages')

class NewsCategory(models.Model):
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
        verbose_name = _("Категорія новин")
        verbose_name_plural = _("Категорії новин")
        ordering = ["id"]

class News(models.Model):
    title = models.CharField(max_length=500, verbose_name=_('Заголовок (українською)'))
    title_en = models.CharField(max_length=500, verbose_name=_('Заголовок (англійською)'), blank=True)
    sub_title = models.TextField(verbose_name=_('Підзаголовок (українською)'), blank=True)
    sub_title_en = models.TextField(verbose_name=_('Підзаголовок (англійською)'), blank=True)

    image = models.ImageField(upload_to='news/%Y', verbose_name=_('Основне зображення'),
                              null=True, blank=True, default=None)

    body = models.TextField(verbose_name=_('Зміст (українською'), blank=True)
    body_en = models.TextField(verbose_name=_('Зміст (англійською)'), blank=True)
    date = models.DateTimeField(verbose_name=_('Дата'))
    category = models.ForeignKey(NewsCategory, on_delete=models.PROTECT, verbose_name=_('Категорія новин'))

    def __str__(self):
        return self.title

    @property
    def localized_title(self):
        lg = get_language()
        localized_title = getattr(self, f'title_{lg}', self.title)
        return localized_title if localized_title else self.title

    @property
    def localized_sub_title(self):
        lg = get_language()
        localized_sub_title = getattr(self, f'sub_title_{lg}', self.sub_title)
        return localized_sub_title if localized_sub_title else self.sub_title

    @property
    def localized_body(self):
        lg = get_language()
        localized_body = getattr(self, f'body_{lg}', self.body)
        return localized_body if localized_body else self.body

    class Meta:
        verbose_name = _("Новина")
        verbose_name_plural = _("Новини")
        ordering = ["-date"]


class NewsImages(models.Model):
    title = models.CharField(max_length=500, verbose_name=_('Заголовок (українською)'), blank=True)
    title_en = models.CharField(max_length=500, verbose_name=_('Заголовок (англійською)'), blank=True)
    news = models.ForeignKey(News, on_delete=models.CASCADE, verbose_name=_('Новина'), )
    image = models.ImageField(upload_to='news/%Y', verbose_name=_('Зображення'),
                              null=True, blank=True, default=None)

    def __str__(self):
        return self.title

    @property
    def localized_title(self):
        lg = get_language()
        localized_title = getattr(self, f'title_{lg}', self.title)
        return localized_title if localized_title else self.title

    class Meta:
        verbose_name = _("Зображення новин")
        verbose_name_plural = _("Зображення новин")
