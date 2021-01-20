from django.urls import path
from .views import index, item_details, items_category, customer_cart


urlpatterns = [
    path('', index, name='index'),
    path('cart/', customer_cart, name='customer_cart'),
    path('<str:category_slug>/<str:item_slug>/', item_details,
         name='item_detail'),
    path('<str:category_slug>/', items_category, name='items_category'),
]
