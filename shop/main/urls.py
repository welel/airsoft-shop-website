from django.urls import path
from .views import index, ItemDetailView


urlpatterns = [
    path('', index, name='index'),
    path('<str:category>/<str:slug>/', ItemDetailView.as_view(),
            name='item_detail'
    ),
]
