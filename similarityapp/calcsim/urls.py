from django.conf.urls import url
from django.urls import path

from .views import TaskCreateView, TaskRetrieveView

app_name = 'calcsim'
urlpatterns = [
    path('calcsim', TaskCreateView.as_view()),
    path('calcsim/<uuid:task_id>', TaskRetrieveView.as_view()),
]
