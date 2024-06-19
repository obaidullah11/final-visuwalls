from django.contrib import admin
from .models import Product, Category,ProductInventory,BookingRequest,ConfirmBooking

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'category', 'quantity', 'weight', 'size', 'power_consumption', 'brightness','status']
    search_fields = ['name', 'category']
    list_filter = ['category', 'quantity', 'weight']

@admin.register(ProductInventory)
class ProductInventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'available_quantity', 'booked_quantity', 'rental_quantity', 'damaged_quantity', 'need_repairing_quantity')



@admin.register(BookingRequest)
class BookingRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'product_inventory', 'quantity', 'request_date', 'status')
    list_filter = ('status',)
    search_fields = ('user__username', 'product_inventory__product__name')

@admin.register(ConfirmBooking)
class ConfirmBookingAdmin(admin.ModelAdmin):
    list_display = ('booking_request', 'product', 'confirmed_date')
    search_fields = ('booking_request__product_inventory__product__name', 'product__name')