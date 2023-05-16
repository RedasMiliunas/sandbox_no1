from django.contrib import admin
from .models import Status, Product, ProductPrice, Order, OrderLine, VehicleModel

class OrderLineInline(admin.TabularInline):
    model = OrderLine
    extra = 0
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'date', 'status']
    inlines = [OrderLineInline]
    list_filter = ['status', 'customer', 'date']
# Register your models here.

admin.site.register(Status)
admin.site.register(Product)
admin.site.register(ProductPrice)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLine)
admin.site.register(VehicleModel)
