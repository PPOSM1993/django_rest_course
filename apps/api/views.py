from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.pagination import (LimitOffsetPagination,PageNumberPagination)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import (ProductFilter, OrderFilter, InStockFilterBackend)
from .models import *
from .serializers import *

from rest_framework.decorators import action

# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.order_by('pk')
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    
    filterset_class = ProductFilter
    filter_backends = [
        DjangoFilterBackend, 
        filters.SearchFilter, 
        filters.OrderingFilter,
        #filters,InStockFilterBackend

    ]

    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'stock']
    
    pagination_class = PageNumberPagination
    pagination_class.page_size = 9
    pagination_class.page_query_param = 'pagenum'
    pagination_class.page_size_query_param ='size'
    pagination_class.max_page_size = 10
    
    def get_permissions(self):
        self.permission_classes = [AllowAny]

        if self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated]

        elif self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]

    pagination_class = None
    filterset_class = OrderFilter

    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend]


    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)
        return qs

    """Crear una funcion que evite que el usuario no pueda crear ordenes si no esta autenticado"""

    @action(
        detail=False, 
        methods=['GET', 'POST'], 
        url_path='user_orders',
        permission_classes = [IsAuthenticated]
    )
    def user_orders(self, request):
        orders = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(orders, many=True)

        return Response(serializer.data)




