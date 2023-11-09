from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.utils.translation import gettext_lazy as _

from reua.models import Project
from reua.views.mixins import BreadCrumbsMixin


__all__ = ('ListProjectView', 'DetailProjectView')

class ListProjectView(BreadCrumbsMixin, ListView):
    model = Project
    template_name = 'projects/projects.html'
    bc = [{'title': _("Актуальні проєкти")}]
    page_title = _("Актуальні проєкти")
    context_object_name = 'projects'


class DetailProjectView(BreadCrumbsMixin, DetailView):
    model = Project
    context_object_name = 'project'
    template_name = 'projects/project.html'

    bc = [
        {'title': _("Актуальні проєкти"), 'url': reverse_lazy('project-list')},
    ]

    def get_bc(self):
        return [*super().get_bc(), {'title': self.get_page_title()}]
    def get_page_title(self):
        return str(self.object)


class DetailWaterProjectView(BreadCrumbsMixin, DetailView):
    model = Project
    context_object_name = 'project'
    template_name = 'projects/water-project.html'

    bc = [
        {'title': _("Актуальні проєкти"), 'url': reverse_lazy('project-list')},
    ]

    def get_bc(self):
        return [*super().get_bc(), {'title': self.get_page_title()}]
    def get_page_title(self):
        return str(self.object)
