from rest_framework import serializers
from .models import *
from rest_framework.validators import UniqueValidator





class CategorycreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=100,
        validators=[UniqueValidator(queryset=Category.objects.all(), message="This category name already exists.")]
    )

    class Meta:
        model = Category
        fields = ('id', 'name')
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'image', 'name', 'category','quantity', 'weight', 'size', 'pitch', 'dynamic_attributes']
class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'

class getFavoriteSerializer(serializers.ModelSerializer):
    Product = ProductSerializer()
    class Meta:
        model = Favorite
        fields = '__all__'

class ProductInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInventory
        fields = ['id','available_quantity', 'booked_quantity', 'rental_quantity', 'damaged_quantity', 'need_repairing_quantity']

class ProductFilterSerializer(serializers.ModelSerializer):
    inventory = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'image', 'name', 'category', 'quantity', 'weight', 'size', 'pitch', 'dynamic_attributes', 'inventory']

    def get_inventory(self, obj):
        inventory = ProductInventory.objects.filter(product=obj).first()
        if inventory:
            return ProductInventorySerializer(inventory).data
        return None
class BookingRequestSerializer(serializers.ModelSerializer):
    product_inventory = serializers.PrimaryKeyRelatedField(queryset=ProductInventory.objects.all())

    class Meta:
        model = BookingRequest
        fields = '__all__'


class BookingUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email','address']

class BookingProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name']

class BookingProductInventorySerializer(serializers.ModelSerializer):
    product = BookingProductSerializer()

    class Meta:
        model = ProductInventory
        fields = ['id', 'product', 'available_quantity', 'booked_quantity', 'rental_quantity', 'damaged_quantity', 'need_repairing_quantity']

class BookingRequestnewSerializer(serializers.ModelSerializer):
    user = BookingUserSerializer()
    product_inventory = BookingProductInventorySerializer()

    class Meta:
        model = BookingRequest
        fields = ['id', 'user', 'product_inventory', 'quantity', 'request_date', 'return_date', 'status']




class ConfirmBookingSerializer(serializers.ModelSerializer):
    booking_request = BookingRequestnewSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = ConfirmBooking
        fields = '__all__'




class RepairingProductSerializer(serializers.ModelSerializer):
    confirm_booking = ConfirmBookingSerializer(read_only=True)
    class Meta:
        model = RepairingProduct
        fields = '__all__'




class RepairingProductStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairingProduct
        fields = ['status']