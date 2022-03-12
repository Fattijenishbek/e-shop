from django.shortcuts import render
from rest_framework import generics, status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from .models import Comment, Product, Reply, Variation, Category
from .serializer import (
    ProductSerializer,
    CommentSerializer,
    VariationSerializer,
    ReplySerializer,
    CategorySerializer,
)
from .permissions import IsSupplier, IsAuthorOrReadOnly
from carts.models import Cart
from orders.models import Order, Promocode
# Create your views here.


class APIHomeView(APIView):
    def get(self, request, format=None):
        data = {
            "authentication": {
                "register": reverse("register_api", request=request),
                "login": reverse("login_api", request=request),
                "token_refresh": reverse("token_refresh", request=request),
                "profile": reverse("user_profile", request=request),
            },
            "products": {
                "count": Product.objects.all().count(),
                "url": reverse("products_api", request=request),
            },
            "product_variations": {
                "count": Variation.objects.all().count(),
                "url": reverse("variations_api", request=request),
            },
            "comments": {
                "count": Comment.objects.all().count(),
                "url": reverse("comments_api", request=request),
            },
            "comment-replies": {
                "count": Reply.objects.all().count(),
                "url": reverse("replies_api", request=request),
            },
            "categories": {
                "count": Category.objects.all().count(),
                "url": reverse("category_list_api", request=request),
            },
            "cart": {
                "count": Cart.objects.all().count(),
                "url": reverse("carts_api", request=request),
                "Here you add the product to your cart": reverse(
                    "add_to_cart_api", request=request
                ),
            },
            "orders": {
                "count": Order.objects.all().count(),
                "url": reverse("orders_api", request=request),
            },
            "checkout": {
                "message": "Here you make a purchase, be careful as soon as you do request, you make an order and your cart gets emptied",
                "url": reverse("checkout_api", request=request),
            },
            "promocodes": {
                "count": Promocode.objects.all().count(),
                "url": reverse("promocode_api", request=request),
            },
        }
        return Response(data)


class ProductList(generics.ListCreateAPIView):
    permission_classes = [IsSupplier]

    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsSupplier]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CommentList(generics.ListCreateAPIView):
    def get(self, request, format=None):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class VariationList(generics.ListAPIView):
    queryset = Variation.objects.all()
    serializer_class = VariationSerializer


class VariationDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsSupplier]
    queryset = Variation.objects.all()
    serializer_class = VariationSerializer


class RepliesList(generics.ListCreateAPIView):
    def get(self, request, format=None):
        replies = Reply.objects.all()
        serializer = ReplySerializer(replies, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ReplySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReplyDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer


class CategoryListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsSupplier]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
