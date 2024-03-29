from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.utils.translation import gettext_lazy as _

from reua.fillters import NewsFilter
from reua.models import News, NewsCategory
from reua.views.mixins import BreadCrumbsMixin

__all__ = ('ListNewsView', 'DetailNewsView')


class ListNewsView(BreadCrumbsMixin, ListView):
    model = News
    template_name = 'news/news-list.html'
    bc = [{'title': _("Прес-центр")}]
    page_title = _("Прес-центр")
    context_object_name = 'news'
    paginate_by = 10
    queryset = News.objects.filter(enabled=True)

    def __init__(self, *args, **kwargs):
        self._filter = None
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        q = super().get_queryset()
        self._filter = NewsFilter(self.request.GET, queryset=q)
        return self._filter.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=object_list, **kwargs)
        ctx['categories'] = NewsCategory.objects.all().annotate(news_count=Count('news')).order_by('id')
        ctx['news_count'] = sum(r.news_count for r in ctx['categories'])
        ctx['current_category'] = self._filter.form.cleaned_data.get('category', None)
        return ctx


class DetailNewsView(BreadCrumbsMixin, DetailView):
    model = News
    context_object_name = 'news'
    template_name = 'news/news-item.html'
    page_title = ''
    queryset = News.objects.filter(enabled=True)

    bc = [
        {'title': _("Прес-центр"), 'url': reverse_lazy('news-list')},
    ]

    def get_bc(self):
        return [*super().get_bc(), {'title': self.object.localized_title}]

    def get_page_title(self):
        return None
        # return self.object.localized_title

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['categories'] = NewsCategory.objects.all().annotate(news_count=Count('news')).order_by('id')
        ctx['current_category'] = self.object.category
        ctx['news_count'] = News.objects.all().count()
        ctx['latest_news'] = News.objects.all().order_by('-date')[:5]
        if (self.object.image):
            ctx['page_image_url'] = self.object.image.url
        return ctx
