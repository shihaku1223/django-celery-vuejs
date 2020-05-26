from django.conf.urls import url
from django.urls import path

from .views import TaskCreateView

app_name = 'calcsim'
urlpatterns = [
    path('calcsim', TaskCreateView.as_view()),
]
