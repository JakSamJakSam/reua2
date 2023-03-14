from .views import *
from django.urls import path, include

# app_name = 'reua'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('feedback/', FeedbackFormView.as_view(), name='feedback'),
    path('company/', ListCompanyView.as_view(), name='company-list'),
    path('company/<int:pk>/', DetailCompanyView.as_view(), name='company-item'),
    path('company/new/', AddCompany.as_view(), name='company-create'),
    path('investition/', ListInvestitionView.as_view(), name='investition-list'),
    path('investition/<int:pk>/', DetailinvestitionView.as_view(), name='investition-item'),
    path('investition/new/', Addinvestition.as_view(), name='investition-create'),
    path('projects/', ListProjectView.as_view(), name='project-list'),
    path('projects/<int:pk>/', DetailProjectView.as_view(), name='project-item'),
    path('water/', WaterView.as_view(), name='water'),
    path('about/', AboutView.as_view(), name='about'),
    path('rebuild/', RebuildView.as_view(), name='rebuild'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('news/', ListNewsView.as_view(), name='news-list'),
    path('news/<int:pk>/', DetailNewsView.as_view(), name='news-item'),
    path('pdf/<int:pk>/', FileView.as_view(), name='pdf-item'),

    path('fp/', include('django.contrib.flatpages.urls')),

]

