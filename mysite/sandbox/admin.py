from django.contrib import admin
from .models import (Status,
                     Product,
                     ProductPrice,
                     Order,
                     OrderLine,
                     VehicleModel,
                     OrderComment,
                     UserProfile,
                     Contacts,
                     ContactsVar,
                     )

class OrderLineInline(admin.TabularInline):
    model = OrderLine
    extra = 0

class OrderCommentInLine(admin.TabularInline):
    model = OrderComment
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'model', 'date', 'status', 'due_back']
    inlines = [OrderLineInline, OrderCommentInLine]
    list_filter = ['status', 'customer', 'model', 'date', 'due_back']
    list_editable = ['status', 'due_back', ]


class OrderReviewAdmin(admin.ModelAdmin):
    list_display = ['order', 'date_created', 'commentator', 'comment']


class ProductPriceAdmin(admin.ModelAdmin):
    list_filter = ['product', 'model', ]

# class ContactsVarInLine(admin.TabularInline):
#     model = ContactsVar
# #     extra = 0

class ContactsVarAdmin(admin.ModelAdmin):
    list_display = ['department', 'email', 'phone', ]
    list_editable = ['email', 'phone', ]


# Register your models here.

admin.site.register(Status)
admin.site.register(Product)
admin.site.register(ProductPrice, ProductPriceAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLine)
admin.site.register(VehicleModel)
admin.site.register(OrderComment, OrderReviewAdmin)
admin.site.register(UserProfile, )
admin.site.register(Contacts, )
admin.site.register(ContactsVar, ContactsVarAdmin)
