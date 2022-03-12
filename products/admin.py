from django.contrib import admin
from .models import Product, Category, Comment, Pictures, Variation, Reply

# Register your models here.

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Pictures)
admin.site.register(Variation)
admin.site.register(Reply)
