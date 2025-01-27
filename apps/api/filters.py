import django_filters
from .models import *
from rest_framework import filters


class InStockFilterBackend(filters.BaseFilterBackend):
    def get_queryset(self, request, queryset, view):
        return queryset.filter(stock__gt=0)


class ProductFilter(django_filters.FilterSet):
    create_at = django_filters.DateFilter(field_name='created_at__date')
    class Meta:
        model = Product
        fields ={
            'name': ['exact', 'contains'],
            'price': ['exact', 'lt', 'gt', 'range']
        }

class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = {
            'status': ['exact'],
            'created_at' : ['lt', 'gt', 'exact']
        }