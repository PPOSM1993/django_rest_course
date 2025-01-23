from rest_framework import serializers
from .models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'description',
            'name',
            'price',
            'stock',
        )

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Price must be greater than 0."
            )
        return value

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (

        )


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem

