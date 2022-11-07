from django.urls import path

from search.views import search_items


urlpatterns = [
    path('', search_items, name='search'),
]
