from django.urls import path
from . import views

urlpatterns = [
    #path('products_list/', views.ProductList, name='product_list'),
    path('products/', views.ProductListAPIView.as_view(), name='products'),
    #path('products/<int:pk>/', views.ProductDetail, name='products'),
    path('products/<int:pk>/', views.ProductDetailAPIView.as_view(), name='products'),
    #path('orders/', views.OrderList, name='orders'),
    path('orders/', views.OrderListAPIView.as_view(), name='orders'),
    path('user_orders/', views.UserOrderListAPIView.as_view(), name='user_orders'),
    path('products/info/', views.ProductInfoAPIView.as_view(), name='info'),
]
