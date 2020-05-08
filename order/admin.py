from django.contrib import admin

# Register your models here.
from order.models import ShopCart


class ShopCartAdmin(admin.ModelAdmin):
    list_display = ['user','product','stok','quantity']
    list_filter = ['user']
admin.site.register(ShopCart,ShopCartAdmin)
