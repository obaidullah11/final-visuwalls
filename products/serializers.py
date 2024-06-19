# from rest_framework import serializers
# import re
# from .models import Product,Category,ProductInventory,BookingRequest,ConfirmBooking
# import base64
# from django.core.files.base import ContentFile
# from django.core.files.storage import default_storage
# from rest_framework.validators import UniqueValidator





# class CategorycreateSerializer(serializers.ModelSerializer):
#     name = serializers.CharField(
#         max_length=100,
#         validators=[UniqueValidator(queryset=Category.objects.all(), message="This category name already exists.")]
#     )

#     class Meta:
#         model = Category
#         fields = ('id', 'name')
# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ('id', 'name')


# class ProductListSerializer(serializers.ListSerializer):
#     def create(self, validated_data):
#         products = [Product(**item) for item in validated_data]
#         return Product.objects.bulk_create(products)

# class ProductSerializer(serializers.ModelSerializer):
#     # category_name = serializers.CharField(source='category', allow_null=True, required=False)

#     class Meta:
#         model = Product
#         fields = '__all__'
#         list_serializer_class = ProductListSerializer
#     def create(self, validated_data):
#         products = []
#         for item in validated_data:
#             # Extract quantity from the quantity data string
#             quantity_string = item.pop('quantity', None)
#             quantity = self.context['child'].extract_numeric_value(quantity_string)
#             product = Product(**item)
#             products.append(product)

#             # Create the product inventory
#             product_inventory = ProductInventory(product=product, available_quantity=quantity)
#             product_inventory.save()

#         return Product.objects.bulk_create(products)
#     # def create(self, validated_data):
#     #     return Product.objects.create(**validated_data)

#     # def create(self, validated_data):
#     #     # Extract quantity from the quantity data string
#     #     quantity_string = validated_data.pop('quantity', None)
#     #     quantity = self.extract_numeric_value(quantity_string)
#     #     # Create the product
#     #     product = Product.objects.create(**validated_data)
#     #     # Associate the product with its inventory
#     #     ProductInventory.objects.create(product=product, available_quantity=quantity)
#     #     return product
#     def extract_numeric_value(self, quantity_string):
#         # Regular expression to extract numeric value
#         pattern = r'\b\d+\b'
#         match = re.search(pattern, quantity_string)
#         if match:
#             return int(match.group())
#         return 0
#     def update(self, instance, validated_data):
#         instance.category = validated_data.get('category', instance.category)
#         instance.image_base64 = validated_data.get('image_base64', instance.image_base64)
#         instance.name = validated_data.get('name', instance.name)
#         instance.quantity = validated_data.get('quantity', instance.quantity)
#         instance.weight = validated_data.get('weight', instance.weight)
#         instance.size = validated_data.get('size', instance.size)
#         instance.pitch = validated_data.get('pitch', instance.pitch)
#         instance.power_consumption = validated_data.get('power_consumption', instance.power_consumption)
#         instance.brightness = validated_data.get('brightness', instance.brightness)
#         instance.viewing_angle = validated_data.get('viewing_angle', instance.viewing_angle)
#         instance.curve = validated_data.get('curve', instance.curve)
#         instance.n_16a_2500w = validated_data.get('n_16a_2500w', instance.n_16a_2500w)
#         instance.n_link = validated_data.get('n_link', instance.n_link)
#         instance.screens_inside_flight_case = validated_data.get('screens_inside_flight_case', instance.screens_inside_flight_case)
#         instance.flight_case_dimensions = validated_data.get('flight_case_dimensions', instance.flight_case_dimensions)
#         instance.flight_case_weight = validated_data.get('flight_case_weight', instance.flight_case_weight)
#         instance.status = validated_data.get('status', instance.status)
#         instance.save()
#         return instance

#     # def get_category_name(self, obj):
#     #     if obj.category:
#     #         return obj.category.name
#     #     return None



# #get product
# class ProductInventorySerializer(serializers.ModelSerializer):
#     product = ProductSerializer()
#     class Meta:
#         model = ProductInventory
#         fields = ['id', 'product','available_quantity', 'booked_quantity', 'rental_quantity', 'damaged_quantity', 'need_repairing_quantity']

# class getdetailProductSerializer(serializers.ModelSerializer):
#     inventory = ProductInventorySerializer()

#     class Meta:
#         model = Product
#         fields = '__all__'

# # class ProductInventorynewSerializer(serializers.ModelSerializer):
# #     product = ProductSerializer()

# #     class Meta:
# #         model = ProductInventory
# #         fields = ['id', 'product', 'available_quantity', 'booked_quantity', 'rental_quantity', 'damaged_quantity', 'need_repairing_quantity']

# class BookingRequestSerializer(serializers.ModelSerializer):
#     product_inventory = ProductInventorySerializer()

#     class Meta:
#         model = BookingRequest
#         fields = '__all__'
# # class ConfirmBookingSerializer(serializers.ModelSerializer):
# #     booking_request = BookingRequestSerializer()



# #     class Meta:
# #         model = ConfirmBooking
# #         fields = ['id', 'booking_request', 'confirmed_date']

# class ConfirmBookingSerializer(serializers.ModelSerializer):
#     booking_request = BookingRequestSerializer()
#     product = ProductSerializer()  # Include product details

#     class Meta:
#         model = ConfirmBooking
#         fields = ['id', 'booking_request', 'product', 'confirmed_date']