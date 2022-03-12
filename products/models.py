from django.db import models
from django.conf import settings

# Create your models here.

rates = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5))


class Category(models.Model):
    name = models.CharField(max_length=250, db_index=True)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    discount = models.IntegerField(default=0)
    supplier = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-title"]

    def __str__(self) -> str:
        return self.title + " / " + str(self.price)


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    discount = models.IntegerField(default=0)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title + " / " + str(self.price) + " / " + str(self.discount) + " % "


class Pictures(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image_url = models.CharField(max_length=200, default="media/images/default.png")


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    rate = models.IntegerField(choices=rates)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:

        return self.content


class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    rate = models.IntegerField(choices=rates)
    creation_date = models.DateTimeField(auto_now_add=True)
