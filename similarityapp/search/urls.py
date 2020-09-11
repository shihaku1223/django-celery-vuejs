from django.conf.urls import url
from django.urls import path

from .views import SearchView
from .views import ESSearchView
from .views import ESScrollView

app_name = 'search'
urlpatterns = [
    path('', ESSearchView.as_view()),
    path('<str:scroll_id>', ESScrollView.as_view()),
]
