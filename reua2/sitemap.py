from django.contrib.sitemaps import Sitemap

from reua.models import TopMenu


class MenuSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    i18n = True
    alternates = True
    x_default = True
    def items(self):
        return TopMenu.objects.filter(disabled=False)

    def location(self, item):
        return item.url

