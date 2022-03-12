from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from decimal import Decimal

from .models import Cart, CartCheckout, CartItem, CartItemCheckout
from .serializer import CartSerializer
from orders.models import Order
from products.models import Variation
# Create your views here.

class CartAPIView(generics.ListAPIView):

    serializer_class = CartSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        cart = Cart.objects.get(user=user)
        serializer = self.serializer_class(cart)
        return Response(serializer.data)


class AddProductToCartAPI(APIView):
    def post(self, request, format=None):
        data = request.data
        user = request.user

        cart = Cart.objects.get(user=user)

        title_price = data.get("product").split("/")
        title = title_price[0].strip()
        price = title_price[1].strip()
        d = title_price[2].strip()
        discount, index = "", 0

        while d[index] != " ":
            discount += d[index]
            index += 1

        quantity = data.get("quantity")

        flash_message = ""

        variation_instance = Variation.objects.filter(
            title=title, price=Decimal(price), discount=int(discount)
        ).last()
        CartItem.objects.create(
            cart=cart, product=variation_instance, quantity=quantity
        )
        flash_message = "Successfully added to the cart"

        response = {
            "message": flash_message,
        }
        return Response(response)


class CheckoutAPIView(APIView):
    def post(self, request, format=None):
        user = request.user
        cart_id = Cart.objects.get(user=user)
        all_items = CartItem.objects.filter(cart=cart_id)

        total_price = 0
        total_price_with_discount = 0

        products = []

        for item in all_items:
            # total_price
            total_price += item.product.price * item.quantity

            # total_price_with_discount
            price = item.product.price
            discount = item.product.discount
            price_after_discount = (price - (price * discount) / 100) * item.quantity
            total_price_with_discount += price_after_discount

            # for order history
            product = CartItemCheckout.objects.create(
                cart=item.cart, product=item.product, quantity=item.quantity
            )
            products.append(product)

        all_items.delete()
        cart = CartCheckout.objects.create(cart=cart_id)
        cart.products.add(*products)

        order = Order.objects.create(
            cart=cart,
            user=user,
            total_order_price=total_price,
            total_order_price_with_discount=total_price_with_discount,
        )
        order_data = {
            "total_order_price": order.total_order_price,
            "total_order_price_with_discount": order.total_order_price_with_discount,
        }

        return Response(order_data)
