from rest_framework import serializers
from .models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'description',
            'price',
            'stock',
        )

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Price must be greater than 0."
            )
        return value



class OrderItemSerializer(serializers.ModelSerializer):

    #product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = (
            'product',
            'quantity', 
            #'product', 
        )

class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(many=True, read_only=True)
    products = ProductSerializer(many=True, read_only=True)

    total_price = serializers.SerializerMethodField() #method_name='total_price'

    def get_total_price(self, obj):
        order_items = obj.items.all()
        return sum(order_item.item_subtotal for order_item in order_items)

    class Meta:
        model = Order
        fields = (
            'order_id',
            'created_at',
            'user',
            'status',
            'products',
            'items',
            'total_price',
        )


class ProductInfoSerializer(serializers.Serializer):
    #Get all products, count of products, max price

    products = ProductSerializer(many=True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField()
