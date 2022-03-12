"""e_shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
from products.views import *
from carts.views import *

from users.views import *
from orders.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", APIHomeView.as_view(), name="home_api"),
    path("api/register/", RegisterView.as_view(), name="register_api"),
    path("api/register/email_verify/", VerifyEmailView.as_view(), name="email_verify"),
    path("api/login/", LoginView.as_view(), name="login_api"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view()),
    path("api/user/profile/", UserRetrieveUpdateAPIView.as_view(), name="user_profile"),
    path("api/cart/", CartAPIView.as_view(), name="carts_api"),
    path("api/cart/add_product/", AddProductToCartAPI.as_view(), name="add_to_cart_api"),
    path("api/orders/", OrderListAPI.as_view(), name="orders_api"),
    path("api/orders/<int:pk>", OrderDetailAPI.as_view(), name="order_detail_api"),
    path("api/checkout/", CheckoutAPIView.as_view(), name="checkout_api"),
    path("api/checkout/<str:promocode>/", GetPriceWithPromocode.as_view(),name="checkout_promocode_api",),
    path("api/products/", ProductList.as_view(), name="products_api"),
    path("api/products/<int:pk>", ProductDetail.as_view(), name="product_api_detail"),
    path("api/products/comments/", CommentList.as_view(), name="comments_api"),
    path("api/products/comments/<int:pk>",CommentDetail.as_view(),name="comment_api_detail",),
    path("api/products/comments/replies/", RepliesList.as_view(), name="replies_api"),
    path("api/products/comments/replies/<int:pk>",ReplyDetail.as_view(),name="reply_detail_api",),
    path("api/products/variations/", VariationList.as_view(), name="variations_api"),
    path("api/products/variations/<int:pk>",VariationDetail.as_view(),name="variation_api_detail",),
    path("api/products/categories/",CategoryListCreate.as_view(),name="category_list_api",),
    path("api/promocodes/",PromocodoApi().as_view(),name="promocode_api",),
]

