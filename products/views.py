# # myapp/views.py
# import re
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.decorators import api_view
# from .serializers import ProductSerializer, ProductListSerializer,CategorySerializer,CategorycreateSerializer,getdetailProductSerializer,BookingRequestSerializer,ConfirmBookingSerializer
# from rest_framework import viewsets
# from .models import Category,Product,ProductInventory,BookingRequest,ConfirmBooking
# from users.models import User
# from django.shortcuts import get_object_or_404




# @api_view(['GET'])
# def all_bookings_for_user(request, user_id):
#     try:
#         user = User.objects.get(pk=user_id)
#     except User.DoesNotExist:
#         return Response({'success': False, 'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

#     # Retrieve all BookingRequest instances for the specific user
#     booking_requests = BookingRequest.objects.filter(user=user)

#     # Serialize BookingRequest instances
#     serializer = BookingRequestSerializer(booking_requests, many=True)
#     data = serializer.data
#     return Response({'success': True, 'message': 'All bookings retrieved successfully', 'data': data}, status=status.HTTP_200_OK)


# # @api_view(['GET'])
# # def confirm_bookings_for_user(request, user_id):
# #     try:
# #         user = User.objects.get(pk=user_id)
# #     except User.DoesNotExist:
# #         return Response({'success': False, 'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

# #     # Retrieve all BookingRequest instances for the specific user with status 'approved'
# #     booking_requests_approved = BookingRequest.objects.filter(
# #         user=user,
# #         status='approved'
# #     )

# #     # Retrieve all ConfirmBooking instances associated with the filtered BookingRequest instances
# #     confirm_bookings = ConfirmBooking.objects.filter(booking_request__in=booking_requests_approved)

# #     # Serialize ConfirmBooking instances
# #     serializer = ConfirmBookingSerializer(confirm_bookings, many=True)
# #     data = serializer.data
# #     return Response({'success': True, 'message': 'Confirm bookings retrieved successfully', 'data': data}, status=status.HTTP_200_OK)

# # from rest_framework.response import Response
# # @api_view(['POST'])
# # def update_booking_request_status(request, booking_request_id):
# #     try:
# #         booking_request = BookingRequest.objects.get(pk=booking_request_id)
# #     except BookingRequest.DoesNotExist:
# #         return Response({'success': False, 'message': 'Booking request does not exist'}, status=status.HTTP_404_NOT_FOUND)

# #     new_status = request.data.get('status')

# #     if new_status not in dict(BookingRequest.STATUS_CHOICES):
# #         return Response({'success': False, 'message': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

# #     if new_status == 'approved':
# #         # Update status and perform inventory adjustment for approved requests
# #         booking_request.status = new_status
# #         booking_request.save()

# #         # Update product inventory
# #         product_inventory = booking_request.product_inventory
# #         product_inventory.available_quantity -= booking_request.quantity
# #         product_inventory.booked_quantity += booking_request.quantity
# #         product_inventory.save()

# #         # Create a confirm booking record
# #         ConfirmBooking.objects.create(booking_request=booking_request, product=product_inventory.product)

# #         return Response({'success': True, 'message': 'Booking request approved and inventory updated'}, status=status.HTTP_200_OK)

# #     # For other statuses, simply update the booking request status
# #     booking_request.status = new_status
# #     booking_request.save()

# #     return Response({'success': True, 'message': 'Booking request status updated'}, status=status.HTTP_200_OK)
# @api_view(['POST'])
# def update_booking_request_status(request, booking_request_id):
#     try:
#         booking_request = BookingRequest.objects.get(pk=booking_request_id)
#     except BookingRequest.DoesNotExist:
#         return Response({'success': False, 'message': 'Booking request does not exist'}, status=status.HTTP_404_NOT_FOUND)

#     new_status = request.data.get('status')

#     if new_status not in dict(BookingRequest.STATUS_CHOICES):
#         return Response({'success': False, 'message': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

#     product_inventory = booking_request.product_inventory

#     if booking_request.status == 'approved' and new_status != 'approved':
#         # Reverse the inventory update for previously approved request
#         product_inventory.available_quantity += booking_request.quantity
#         product_inventory.booked_quantity -= booking_request.quantity
#         product_inventory.save()

#         # If there's a ConfirmBooking record, delete it
#         ConfirmBooking.objects.filter(booking_request=booking_request).delete()

#     if new_status == 'approved':
#         # Update status and perform inventory adjustment for approved requests
#         booking_request.status = new_status
#         booking_request.save()

#         # Update product inventory
#         product_inventory.available_quantity -= booking_request.quantity
#         product_inventory.booked_quantity += booking_request.quantity
#         product_inventory.save()

#         # Create a confirm booking record
#         ConfirmBooking.objects.create(booking_request=booking_request, product=product_inventory.product)

#         return Response({'success': True, 'message': 'Booking request approved and inventory updated'}, status=status.HTTP_200_OK)

#     # For other statuses, simply update the booking request status
#     booking_request.status = new_status
#     booking_request.save()

#     return Response({'success': True, 'message': 'Booking request status updated'}, status=status.HTTP_200_OK)

# # @api_view(['POST'])
# # def create_booking_request(request):
# #     serializer = BookingRequestSerializer(data=request.data)
# #     if serializer.is_valid():
# #         product_inventory = serializer.validated_data.get('product_inventory')
# #         requested_quantity = serializer.validated_data.get('quantity')

# #         # Check if the requested quantity is available
# #         if product_inventory.available_quantity >= requested_quantity:
# #             # Update the available quantity in the inventory
# #             product_inventory.available_quantity -= requested_quantity
# #             product_inventory.booked_quantity += requested_quantity
# #             product_inventory.save()

# #             # Save the booking request
# #             serializer.save()
# #             return Response({
# #                 'success': True,
# #                 'message': 'Booking request created successfully.',
# #                 'data': serializer.data
# #             }, status=status.HTTP_201_CREATED)
# #         else:
# #             return Response({
# #                 'success': False,
# #                 'message': 'Insufficient quantity available.',
# #                 'data': {}
# #             }, status=status.HTTP_400_BAD_REQUEST)
# #     else:
# #         return Response({
# #             'success': False,
# #             'message': 'Invalid data.',
# #             'data': serializer.errors
# #         }, status=status.HTTP_400_BAD_REQUEST)




# @api_view(['POST'])
# def create_booking_request(request):
#     serializer = BookingRequestSerializer(data=request.data)
#     if serializer.is_valid():
#         product_inventory = serializer.validated_data.get('product_inventory')
#         requested_quantity = serializer.validated_data.get('quantity')

#         # Check if the requested quantity is available
#         if product_inventory.available_quantity >= requested_quantity:
#             # Save the booking request without updating the inventory
#             serializer.save()
#             return Response({
#                 'success': True,
#                 'message': 'Booking request created successfully.',
#                 'data': serializer.data
#             }, status=status.HTTP_201_CREATED)
#         else:
#             return Response({
#                 'success': False,
#                 'message': 'Insufficient quantity available.',
#                 'data': {}
#             }, status=status.HTTP_400_BAD_REQUEST)
#     else:
#         return Response({
#             'success': False,
#             'message': 'Invalid data.',
#             'data': serializer.errors
#         }, status=status.HTTP_400_BAD_REQUEST)







# @api_view(['GET'])
# def product_inventory_api(request):
#     try:
#         products = Product.objects.all()
#         product_list = []

#         for product in products:
#             product_data = {
#                 'id': product.id,
#                 'category': product.category,
#                 'image_base64': product.image_base64,
#                 'name': product.name,
#                 'quantity': product.quantity,
#                 'weight': product.weight,
#                 'size': product.size,
#                 'pitch': product.pitch,
#                 'power_consumption': product.power_consumption,
#                 'brightness': product.brightness,
#                 'viewing_angle': product.viewing_angle,
#                 'curve': product.curve,
#                 'n_16a_2500w': product.n_16a_2500w,
#                 'n_link': product.n_link,
#                 'screens_inside_flight_case': product.screens_inside_flight_case,
#                 'flight_case_dimensions': product.flight_case_dimensions,
#                 'flight_case_weight': product.flight_case_weight,
#                 'status': product.status,
#                 'inventory': [
#                     {
#                         'inventory_id': inventory.id,
#                         'available_quantity': inventory.available_quantity,
#                         'booked_quantity': inventory.booked_quantity,
#                         'rental_quantity': inventory.rental_quantity,
#                         'damaged_quantity': inventory.damaged_quantity,
#                         'need_repairing_quantity': inventory.need_repairing_quantity,
#                     } for inventory in product.inventory.all()
#                 ]
#             }
#             product_list.append(product_data)

#         return Response({
#             'success': True,
#             'message': 'Product inventory fetched successfully.',
#             'data': product_list
#         })
#     except Exception as e:
#         return Response({
#             'success': False,
#             'message': str(e),
#             'data': []
#         })
# @api_view(['GET'])
# def get_all_products(request):
#     if request.method == 'GET':
#         products = Product.objects.all()
#         serializer = ProductSerializer(products, many=True)
#         return Response({
#             'success': True,
#             'message': 'Products retrieved successfully',
#             'data': serializer.data
#         }, status=status.HTTP_200_OK)
# # @api_view(['POST'])
# # def create_products(request):
# #     if request.method == 'POST':
# #         serializer = ProductSerializer(data=request.data, many=True)
# #         if serializer.is_valid():
# #             serializer.save()
# #             created_products = serializer.data
# #             return Response({
# #                 'success': True,
# #                 'message': 'Products created successfully',
# #                 'data': created_products
# #             }, status=status.HTTP_201_CREATED)
# #         return Response({
# #             'success': False,
# #             'message': 'Failed to create products',
# #             'errors': serializer.errors
# #         }, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def create_products(request):
#     if request.method == 'POST':
#         serializer = ProductSerializer(data=request.data, many=True)
#         if serializer.is_valid():
#             products = []
#             for product_data in serializer.validated_data:
#                 quantity_string = product_data.pop('quantity', None)
#                 quantity = serializer.child.extract_numeric_value(quantity_string)
#                 product = Product.objects.create(**product_data)
#                 products.append(product)
#                 ProductInventory.objects.create(product=product, available_quantity=quantity)
#             return Response({
#                 'success': True,
#                 'message': 'Products created successfully',
#                 'data': serializer.data
#             }, status=status.HTTP_201_CREATED)
#         return Response({
#             'success': False,
#             'message': 'Failed to create products',
#             'errors': serializer.errors
#         }, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET'])
# def category_list(request):
#     if request.method == 'GET':
#         categories = Category.objects.all()
#         serializer = CategorySerializer(categories, many=True)
#         data = {
#             'success': True,
#             'message': 'Categories retrieved successfully',
#             'data': serializer.data
#         }
#         return Response(data, status=status.HTTP_200_OK)

# @api_view(['POST'])
# def category_create(request):
#     if request.method == 'POST':
#         serializer = CategorycreateSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             data = {
#                 'success': True,
#                 'message': 'Category created successfully',
#                 'data': serializer.data
#             }
#             return Response(data, status=status.HTTP_201_CREATED)
#         errors = serializer.errors
#         if 'name' in errors and 'This category name already exists.' in errors['name']:
#             return Response({'success': False, 'message': 'Category name must be unique'}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# def category_detail(request, pk):
#     category = get_object_or_404(Category, pk=pk)

#     if request.method == 'GET':
#         serializer = CategorySerializer(category)
#         data = {
#             'success': True,
#             'message': 'Category retrieved successfully',
#             'data': serializer.data
#         }
#         return Response(data, status=status.HTTP_200_OK)

#     elif request.method == 'PUT':
#         serializer = CategorySerializer(category, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             data = {
#                 'success': True,
#                 'message': 'Category updated successfully',
#                 'data': serializer.data
#             }
#             return Response(data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         category.delete()
#         data = {
#             'success': True,
#             'message': 'Category deleted successfully'
#         }
#         return Response(data, status=status.HTTP_204_NO_CONTENT)




# @api_view(['PUT'])
# def update_product(request, pk):
#     try:
#         product = Product.objects.get(pk=pk)
#     except Product.DoesNotExist:
#         return Response({'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'PUT':
#         serializer = ProductSerializer(product, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             updated_product = serializer.data
#             return Response({
#                 'success': True,
#                 'message': 'Product updated successfully',
#                 'data': updated_product
#             }, status=status.HTTP_200_OK)
#         return Response({
#             'success': False,
#             'message': 'Failed to update product',
#             'errors': serializer.errors
#         }, status=status.HTTP_400_BAD_REQUEST)




# @api_view(['DELETE'])
# def delete_product(request, pk):
#     try:
#         product = Product.objects.get(pk=pk)
#     except Product.DoesNotExist:
#         return Response({'success': False, 'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'DELETE':
#         product.delete()
#         return Response({'success': True, 'message': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)