from django.contrib import admin
from api.models import Order, OrderItem, Address, User, Coupon, Post, Comment, Category, Product, Market, Farmer

class OrderItemInlines(admin.TabularInline):
    model = OrderItem
    
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemInlines
    ]
    
    
admin.site.register(Order, OrderAdmin)
admin.site.register(Address)
admin.site.register(User)
admin.site.register(Coupon)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Market)
admin.site.register(Farmer)
