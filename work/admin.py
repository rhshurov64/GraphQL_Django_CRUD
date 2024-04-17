from django.contrib import admin

# Register your models here.
from .models import Category, Product, Post, Writer

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Post)
admin.site.register(Writer)

