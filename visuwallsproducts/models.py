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




# from django.db import models

class ImageUpload(models.Model):
    image = models.ImageField(upload_to='productimages/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image uploaded at {self.uploaded_at}"

# Create your models here.
# from django.db import models

class Product(models.Model):
    category = models.CharField(blank=True, max_length=255)
    image = models.ImageField(upload_to='productimages/', default='productimages/default.png')
    name = models.CharField(max_length=255)  # Renamed from Name(Model) for simplicity
    quantity = models.CharField(max_length=255)
    weight = models.CharField(blank=True, max_length=255)  # Weight in Kg
    size = models.CharField(blank=True, max_length=255)  # Size in mm
    pitch = models.CharField(blank=True, max_length=255)
    dynamic_attributes = models.JSONField(default=dict)


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)



    def __str__(self):
        return f"{self.user.username} - {self.Product}"



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
    project_name = models.CharField(max_length=255, null=True, blank=True)
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
    STATUS_CHOICES = [
        ('BOOKING_APPROVED', 'Booking Approved'),
        ('SEND_PRODUCT_TO_USER', 'Send Product to User'),
        ('RECEIVED_PRODUCT_BY_USER', 'Received Product by User'),
        ('RETURNED', 'Returned'),
    ]


    booking_request = models.OneToOneField(BookingRequest, on_delete=models.CASCADE, related_name='confirm_booking')
    confirmed_date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='BOOKING_APPROVED')

    def __str__(self):
        return f"ConfirmBooking for {self.booking_request.product_inventory.product.name} "

class RepairingProduct(models.Model):
    STATUS_CHOICES = [
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    ]

    confirm_booking = models.ForeignKey(ConfirmBooking, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='IN_PROGRESS')

    def __str__(self):
        return f"Repairing Product for {self.confirm_booking}"

class DamagedProduct(models.Model):
    confirm_booking = models.ForeignKey(ConfirmBooking, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"Damaged Product for {self.confirm_booking}"