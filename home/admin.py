from django.contrib import admin

from home.models import Contact, Order, OrderItem, Product

# Register your models here.
admin.site.register(Contact)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
# admin.site.register(my_orders)
