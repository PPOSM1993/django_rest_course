from django.shortcuts import render
from django.db.models import Max
from .serializers import *
from .models import *
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    AllowAny
)
from rest_framework.views import APIView

# Create your views here.


#Vistas basadas en clases.
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        self.permission_classes = [AllowAny]

        #Condicion que solo me permite crear nuevos productos
        #solo si el usuario esta autenticado.
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]

        #Condicion que me indica que solo podre listar los productos
        #solo si el usuario esta autenticado
        elif self.request.method == 'GET':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(stock__gt=0)
    serializer_class = ProductSerializer

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'GET':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer



class UserOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

class ProductInfoAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer({
            'products': products,
            'count': len(products),
            'max_price': products.aggregate(max_price=Max('price'))['max_price']
        })
        return Response(serializer.data)
    
    def post(self, request):
        pass



#Vista basa en funciones, las cuales nos permiten crear, actualizar, listar y eliminar informacion, mediante la implementacion de una API
"""
@api_view(["GET"])
def ProductList(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)
"""

"""
@api_view(["GET"])
def ProductDetail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)
"""
"""
@api_view(["GET"])
def OrderList(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)
    """

"""
@api_view(['GET'])
def ProductsInfo(request):
    products = Product.objects.all()
    serializer = ProductInfoSerializer({
        'products': products,
        'count': len(products),
        'max_price': products.aggregate(max_price=Max('price'))['max_price']
    })
    return Response(serializer.data)
"""