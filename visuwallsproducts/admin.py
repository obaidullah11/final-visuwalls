from django.contrib import admin
from .models import *
@admin.register(RepairingProduct)
class RepairingProductAdmin(admin.ModelAdmin):
    list_display = ('confirm_booking', 'quantity', 'status')
    list_filter = ('status',)
    search_fields = ('confirm_booking__booking_request__product_inventory__product__name', 'confirm_booking__user__username')

@admin.register(DamagedProduct)
class DamagedProductAdmin(admin.ModelAdmin):
    list_display = ('confirm_booking', 'quantity')
    search_fields = ('confirm_booking__booking_request__product_inventory__product__name', 'confirm_booking__user__username')
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'name','category', 'quantity', 'weight', 'size', 'pitch','get_dynamic_attributes']
    search_fields = ['name', 'category']
    list_filter = ['quantity', 'weight']
    ordering = ['id']

    # Displaying the dynamic attributes in the admin
    def get_dynamic_attributes(self, obj):
        return obj.dynamic_attributes

    get_dynamic_attributes.short_description = 'Dynamic Attributes'





@admin.register(ProductInventory)
class ProductInventoryAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'available_quantity', 'booked_quantity', 'rental_quantity', 'damaged_quantity', 'need_repairing_quantity')

    def product_name(self, obj):
        return obj.product.name

    product_name.admin_order_field = 'product'  # Allows column to be sortable
    product_name.short_description = 'Product Name'  # Renames column head


from django.contrib import admin
from .models import Product, Category,ProductInventory,BookingRequest,ConfirmBooking

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(BookingRequest)
class BookingRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'product_inventory', 'quantity', 'request_date', 'status')
    list_filter = ('status',)
    search_fields = ('user__username', 'product_inventory__product__name')

@admin.register(ConfirmBooking)
class ConfirmBookingAdmin(admin.ModelAdmin):
    list_display = ('booking_request', 'product', 'confirmed_date')
    search_fields = ('booking_request__product_inventory__product__name', 'product__name')