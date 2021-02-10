from django.urls import path

from .views import (
    add_to_cart,
    change_cart_item_quantity,
    clear_cart,
    customer_cart,
    delete_from_cart,
    index,
    item_details,
    items_category,
    logout_,
    make_order,
    signin,
    signup
)


urlpatterns = [
    path('', index, name='index'),
    path('details/<str:category_slug>/<str:item_slug>/', item_details,
         name='item_detail'),
    path('category/<str:category_slug>/', items_category,
         name='items_category'),
    path('cart/', customer_cart, name='customer_cart'),
    path('add_to_cart/<str:category_slug>/<str:item_slug>/', add_to_cart,
         name='add_to_cart'),
    path('delete_from_cart/<str:category_slug>/<str:item_slug>/',
         delete_from_cart, name='delete_from_cart'),
    path('clear_cart/', clear_cart, name='clear_cart'),
    path('checkout/', make_order, name='checkout'),
    path('change_qty/<str:category_slug>/<str:item_slug>/',
         change_cart_item_quantity, name='change_cart_item_quantity'),
    path('signin/', signin, name='signin'),
    path('logout/', logout_, name='logout'),
    path('signup/', signup, name='signup'),
]
