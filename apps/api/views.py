from django.shortcuts import render
from django.db.models import Max
from .serializers import *
from .models import *
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

# Create your views here.


#Vistas basadas en clases.
class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(stock__gt=0)
    serializer_class = ProductSerializer


class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer


class UserOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

#Vista basa en funciones.
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