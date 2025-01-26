import django_filters
from .models import *
from rest_framework import filters


#class InStockFilterBackend(filters.BaseFilterBackend):
#    def get_queryset(self, request, queryset, view):
#        return queryset.filter(stock__gt=0)


class ProductFilter(django_filters.FilterSet):
    class Meta:
        fields ={
            'name': ['exact', 'contains'],
            'price': ['exact', 'lt', 'gt', 'range']
        }