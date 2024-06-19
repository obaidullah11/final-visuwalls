from django.db import models
from users.models import User

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

# class Product(models.Model):
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
#     image_base64 = models.TextField(blank=True, null=True, help_text="Base64-encoded image")
#     name = models.CharField(max_length=255, blank=True)
#     quantity = models.IntegerField(null=True, blank=True)
#     weight = models.FloatField(null=True, blank=True, help_text="Weight in Kg")
#     size = models.CharField(max_length=255, blank=True, help_text="Size in mm")
#     pitch = models.CharField(max_length=255, blank=True)
#     power_consumption = models.CharField(max_length=255, blank=True)
#     brightness = models.CharField(max_length=255, blank=True)
#     viewing_angle = models.CharField(max_length=255, blank=True)
#     curve = models.CharField(max_length=255, blank=True)
#     n_16a_2500w = models.CharField(max_length=255, blank=True, help_text="N/16A(2500w)")
#     n_link = models.CharField(max_length=255, blank=True, help_text="N/Link")
#     screens_inside_flight_case = models.IntegerField(null=True, blank=True)
#     flight_case_dimensions = models.CharField(max_length=255, blank=True, help_text="Flight Case Dimensions (mm)")
#     flight_case_weight = models.FloatField(null=True, blank=True, help_text="Flight Case Weight in kg")

#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name = "Product"
#         verbose_name_plural = "Products"
class Product(models.Model):
    STATUS_CHOICES = (
        ('availible', 'Availible'),
        ('booked', 'Booked'),
        ('damage', 'Damage'),
        ('need_repairing', 'Need Repairing'),
        ('sold', 'Sold'),
    )

    category = models.CharField(max_length=255, blank=True, null=True)
    image_base64 = models.TextField(blank=True, null=True, help_text="Base64-encoded image")
    name = models.CharField(max_length=255, blank=True)
    quantity = models.CharField(max_length=255, blank=True)
    weight = models.FloatField(null=True, blank=True, help_text="Weight in Kg")
    size = models.CharField(max_length=255, blank=True, help_text="Size in mm")
    pitch = models.CharField(max_length=255, blank=True)
    power_consumption = models.CharField(max_length=255, blank=True)
    brightness = models.CharField(max_length=255, blank=True)
    viewing_angle = models.CharField(max_length=255, blank=True)
    curve = models.CharField(max_length=255, blank=True)
    n_16a_2500w = models.CharField(max_length=255, blank=True, help_text="N/16A(2500w)")
    n_link = models.CharField(max_length=255, blank=True, help_text="N/Link")
    screens_inside_flight_case = models.IntegerField(null=True, blank=True)
    flight_case_dimensions = models.CharField(max_length=255, blank=True, help_text="Flight Case Dimensions (mm)")
    flight_case_weight = models.FloatField(null=True, blank=True, help_text="Flight Case Weight in kg")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='availible')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"



class ProductInventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventory')
    available_quantity = models.IntegerField(default=0)
    booked_quantity = models.IntegerField(default=0)  # New field for tracking booked quantity
    rental_quantity = models.IntegerField(default=0)
    damaged_quantity = models.IntegerField(default=0)  # New field for tracking damaged quantity
    need_repairing_quantity = models.IntegerField(default=0)  # New field for tracking quantity needing repair

    def __str__(self):
        return f"Inventory of {self.product.name}"


class BookingRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),

    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='booking_requests')
    product_inventory = models.ForeignKey(ProductInventory, on_delete=models.CASCADE, related_name='booking_requests')
    quantity = models.IntegerField()
    request_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"BookingRequest by {self.user.username} for {self.product_inventory.product.name}"

    class Meta:
        verbose_name = "Booking Request"
        verbose_name_plural = "Booking Requests"
class ConfirmBooking(models.Model):

    booking_request = models.OneToOneField(BookingRequest, on_delete=models.CASCADE, related_name='confirm_booking')
    confirmed_date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"ConfirmBooking for {self.booking_request.product_inventory.product.name} "