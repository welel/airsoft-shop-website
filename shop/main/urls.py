from django.urls import path
from .views import index, ProductDetailView


urlpatterns = [
    path('', index, name='index'),
    path('products/<str:ct_model>/<str:slug>/', ProductDetailView.as_view(),
            name='product_detail'
    ),
]
