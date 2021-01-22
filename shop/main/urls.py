from django.urls import path
from .views import (
    index,
    item_details,
    items_category,
    customer_cart,
    add_to_cart,
    delete_from_cart,
    change_cart_item_quantity
)


urlpatterns = [
    path('', index, name='index'),
    path('cart/', customer_cart, name='customer_cart'),
    path('change_qty/<str:category_slug>/<str:item_slug>/',
         change_cart_item_quantity, name='change_cart_item_quantity'),
    path('add_to_cart/<str:category_slug>/<str:item_slug>/', add_to_cart,
         name='add_to_cart'),
    path('delete_from_cart/<str:category_slug>/<str:item_slug>/',
         delete_from_cart, name='delete_from_cart'),
    path('<str:category_slug>/<str:item_slug>/', item_details,
         name='item_detail'),
    # TODO: Add some prefix to path.
    path('<str:category_slug>/', items_category, name='items_category'),
]
