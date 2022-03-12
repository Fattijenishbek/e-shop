from rest_framework import serializers
from .models import CartItem, Cart, CartItemCheckout, CartCheckout
from decimal import Decimal
from products.serializer import VariationSerializer


class CartItemSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    total_price_with_discount = serializers.SerializerMethodField()
    product = VariationSerializer()

    class Meta:
        model = CartItem
        fields = [
            "cart",
            "product",
            "quantity",
            "total_price",
            "total_price_with_discount",
        ]

    def get_total_price(self, obj):

        total_price = Decimal(obj.product.price) * Decimal(obj.quantity)
        return total_price

    def get_total_price_with_discount(self, obj):

        price = obj.product.price
        discount = obj.product.discount
        price_after_discount = (
            Decimal(price) - Decimal((Decimal(price) * discount) / 100)
        ) * obj.quantity
        return price_after_discount


class CartSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    total_price_with_discount = serializers.SerializerMethodField()
    products = CartItemSerializer(many=True, read_only=True, source="cartitem_set")

    class Meta:
        model = Cart
        fields = ["products", "total_price", "total_price_with_discount"]

    def get_total_price(self, obj):

        cart_id = obj.id
        cart_items = CartItem.objects.filter(cart=cart_id)
        price = 0
        for item in cart_items:
            price += Decimal(item.product.price) * Decimal(item.quantity)
        return price

    def get_total_price_with_discount(self, obj):
        cart_id = obj.id
        cart_items = CartItem.objects.filter(cart=cart_id)
        total_price = 0
        for item in cart_items:
            price = item.product.price
            discount = item.product.discount
            price_after_discount = (
                Decimal(price) - Decimal((Decimal(price) * discount) / 100)
            ) * item.quantity
            total_price += price_after_discount

        return total_price


class CartItemCheckoutSerializer(serializers.ModelSerializer):
    product = VariationSerializer()

    class Meta:
        model = CartItemCheckout
        fields = ["cart", "product", "quantity"]


class CartCheckoutSerializer(serializers.ModelSerializer):
    products = CartItemCheckoutSerializer(many=True, read_only=True)

    class Meta:
        model = CartCheckout
        fields = ["cart", "products"]
