from django.contrib import admin
from .models import *



# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemInline
    ]


admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
admin.site.register(User)


admin.site.register(OrderItem)