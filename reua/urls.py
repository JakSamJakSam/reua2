from .views import *
from django.urls import path, include

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('/feedback/', FeedbackFormView.as_view(), name='feedback'),
    path('/fp/', include('django.contrib.flatpages.urls')),
]

