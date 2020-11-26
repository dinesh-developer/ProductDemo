from django.contrib import admin
from .models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'color', 'price', 'discount', 'is_active')
    search_fields = ('name', 'brand')
    list_filter = ('is_active',)

admin.site.register(Product, ProductAdmin)


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_active',)

admin.site.register(Brand, BrandAdmin)