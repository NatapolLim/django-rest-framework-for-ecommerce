from django.contrib import admin
from .models import OrderItem, Order

# Register your models here.
admin.site.register(OrderItem)

class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'start_date']
admin.site.register(Order, OrderAdmin)
# admin.site.register(BillOrder)