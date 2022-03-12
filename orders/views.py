from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from decimal import Decimal
from products.permissions import IsSupplier, IsOwner
from .models import Order, Promocode
from .serializer import OrderSerializer, PromocodeSerializer

# Create your views here.


class OrderListAPI(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        orders = Order.objects.filter(user=user)
        serializer = self.serializer_class(orders, many=True)
        return Response(serializer.data)


class OrderDetailAPI(generics.RetrieveAPIView):

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        order = self.get_object(pk)
        serializer = self.serializer_class(order)
        return Response(serializer.data)


class PromocodoApi(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsSupplier]
    queryset = Promocode.objects.all()
    serializer_class = PromocodeSerializer


class GetPriceWithPromocode(APIView):
    def get_object(self, promocode):
        try:
            return Promocode.objects.get(name=promocode)
        except Promocode.DoesNotExist:
            raise Http404

    def get(self, request, promocode, format=None):
        promo = self.get_object(promocode)
        user = request.user
        order = Order.objects.filter(user=user).last()
        price = order.total_order_price
        price_with_discount = order.total_order_price_with_discount
        price_after_promocode = Decimal(price) - (Decimal(price) * promo.discount) / 100
        price_with_discount_after_promocode = (
            Decimal(price_with_discount)
            - (Decimal(price_with_discount) * promo.discount) / 100
        )
        data = {
            "total_price_after_promocode": price_after_promocode,
            "total_price_with_discount_after_promocode": price_with_discount_after_promocode,
        }
        return Response(data)
