from django.urls import path
from . import views

urlpatterns = [
    path('products_list/', views.ProductList, name='product_list'),
    path('products/<int:pk>/', views.ProductDetail, name='products'),
]
