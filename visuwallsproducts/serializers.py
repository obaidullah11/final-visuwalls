from rest_framework import serializers
from .models import *
from rest_framework.validators import UniqueValidator

class ConfirmBookingNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfirmBooking
        fields = ['confirmed_date', 'status']

class BookingRequestNestedSerializer(serializers.ModelSerializer):
    confirm_booking = ConfirmBookingNestedSerializer(read_only=True)

    class Meta:
        model = BookingRequest
        fields = '__all__'


class ConfirmBookingSerializeruser(serializers.ModelSerializer):
    class Meta:
        model = ConfirmBooking
        fields = ['status']


class ImageNameField(serializers.Field):
    def to_representation(self, value):
        return value.name

    def to_internal_value(self, data):
        if isinstance(data, str):
            return data
        raise serializers.ValidationError("Invalid image name")
class ProductSerializern(serializers.ModelSerializer):
    image = ImageNameField()

    class Meta:
        model = Product
        fields = '__all__'

# class ImageUploadSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ImageUpload
#         fields = ['id', 'image', 'uploaded_at']

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
    confirm_booking = ConfirmBookingNestedSerializer(read_only=True)

    class Meta:
        model = BookingRequest
        fields = ['id','project_name', 'confirm_booking','user', 'product_inventory', 'quantity', 'request_date', 'return_date', 'status']
class BookingRequestNestedSerializer(serializers.ModelSerializer):
    confirm_booking = ConfirmBookingNestedSerializer(read_only=True)
    product_inventory = BookingProductInventorySerializer()


    class Meta:
        model = BookingRequest
        fields = '__all__'
class ConfirmBookingSerializernew(serializers.ModelSerializer):
    class Meta:
        model = ConfirmBooking
        fields = '__all__'
        depth = 2  # This will allow nested serialization to include related BookingRequest and Product details


class ConfirmBookingSerializer(serializers.ModelSerializer):
    booking_request = BookingRequestnewSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = ConfirmBooking
        fields = '__all__'


class DamagedProductSerializer(serializers.ModelSerializer):
    confirm_booking = ConfirmBookingSerializer(read_only=True)
    class Meta:
        model = DamagedProduct
        fields = ['id', 'confirm_booking', 'quantity']

class RepairingProductSerializer(serializers.ModelSerializer):
    confirm_booking = ConfirmBookingSerializer(read_only=True)


    class Meta:
        model = RepairingProduct
        fields = '__all__'





class RepairingProductStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairingProduct
        fields = ['status']


class ProductFilternewSerializer(serializers.ModelSerializer):
    inventory = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()
    favorite_id = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'image', 'name', 'category', 'quantity', 'weight', 'size', 'pitch', 'dynamic_attributes', 'inventory', 'is_favorite','favorite_id']

    def get_inventory(self, obj):
        inventory = ProductInventory.objects.filter(product=obj).first()
        if inventory:
            return ProductInventorySerializer(inventory).data
        return None

    def get_is_favorite(self, obj):
        user = self.context.get('user')
        if user:
            return Favorite.objects.filter(user=user, Product=obj).exists()
        return False
    def get_favorite_id(self, obj):
        user = self.context.get('user')
        if user:
            favorite = Favorite.objects.filter(user=user, Product=obj).first()
            if favorite:
                return favorite.id
        return None