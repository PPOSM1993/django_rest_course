from rest_framework import serializers
from .models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            #'id',
            'name',
            'description',
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
    
class OrderCreateSerializer(serializers.ModelSerializer):

    class OrderItemCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = OrderItem
            
    order_id = serializers.UUIDField(read_only=True)
    items = OrderItemCreateSerializer(many=True)

    def create(self, validated_data):
        orderitem_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        for item in orderitem_data:
            OrderItem.objects.create(order=order, **item)

            return order

    class Meta:
        model = Order
        fields = (
            'order_id',
            'created_at',
            'user',
            'status',
            'items',
            'total_price',
        )

class OrderSerializer(serializers.ModelSerializer):
    order_id = serializers.UUIDField(read_only=True)
    items = OrderItemSerializer(many=True)
    #products = ProductSerializer(many=True, read_only=True)

    total_price = serializers.SerializerMethodField(method_name='total')

    def total(self, obj):
        order_items = obj.items.all()
        return sum(order_item.item_subtotal for order_item in order_items)

    class Meta:
        model = Order
        fields = (
            'order_id',
            'created_at',
            'user',
            'status',
            #'products',
            'items',
            'total_price',
        )




class ProductInfoSerializer(serializers.Serializer):
    #Get all products, count of products, max price

    products = ProductSerializer(many=True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField()
