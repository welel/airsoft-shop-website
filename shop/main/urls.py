from django.urls import path
from .views import index, item_details


urlpatterns = [
    path('', index, name='index'),
    path('<str:category>/<str:slug>/', item_details, name='item_detail'),
]
