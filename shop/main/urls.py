from django.urls import path
from .views import testv, ProductDetailView


urlpatterns = [
    path('', testv, name='index'),
    path('products/<str:ct_model>/<str:slug>/', ProductDetailView.as_view(),
            name='product_detail'
    ),
]
