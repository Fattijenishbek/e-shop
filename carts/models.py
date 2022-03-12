from products.models import Variation
from django.db import models
from django.conf import settings
# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Variation, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class CartItemCheckout(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Variation, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class CartCheckout(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    products = models.ManyToManyField(CartItemCheckout)
