from django.shortcuts import render
from .serializers import *
from .models import *
from django.http import JsonResponse
from rest_framework.response import Response

from rest_framework.decorators import api_view

from django.shortcuts import get_object_or_404

# Create your views here.



@api_view(["GET"])
def ProductList(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def ProductDetail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)