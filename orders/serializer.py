from django.db.models import fields
from rest_framework import serializers
from .models import Order, Promocode
from carts.serializer import CartCheckoutSerializer


class OrderSerializer(serializers.ModelSerializer):
    cart = CartCheckoutSerializer()

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "cart",
            "created_at",
            "total_order_price",
            "total_order_price_with_discount",
        ]


class PromocodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promocode
        fields = ["name", "discount"]
