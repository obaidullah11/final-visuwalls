import csv
from rest_framework.views import APIView
import json
import re
from rest_framework.response import Response
from rest_framework import generics
from datetime import timedelta
from django.http import HttpResponse, JsonResponse
from numbers_parser import Document
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import*
from .models import *
from django.views.decorators.csrf import csrf_exempt
import re

from rest_framework.exceptions import ParseError

@api_view(['GET'])
def search_product(request):
    query = request.query_params.get('name', None)
    if query is not None:
        products = Product.objects.filter(name__icontains=query)
        serializer = ProductSerializer(products, many=True)
        return Response({
            "success": True,
            "message": "Products retrieved successfully.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            "success": False,
            "message": "Name parameter is required.",
            "data": []
        }, status=status.HTTP_400_BAD_REQUEST)
class AddFavoriteView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = FavoriteSerializer(data=request.data)
        if serializer.is_valid():
            user_id = request.data.get('user')
            product_id = request.data.get('Product')

            # Check if the favorite already exists
            if Favorite.objects.filter(user=user_id, Product=product_id).exists():
                return Response({
                    "success": False,
                    "message": "Favorite already exists for this user and product.",
                    "errors": {
                        "non_field_errors": [
                            "Favorite already exists for this user and product."
                        ]
                    }
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response({
                "success": True,
                "message": "Favorite added successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "success": False,
                "message": "Error adding favorite",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class RemoveFavoriteView(APIView):
    def delete(self, request, favorite_id, *args, **kwargs):
        try:
            favorite = Favorite.objects.get(id=favorite_id)
            favorite.delete()
            return Response({"success": True, "message": "Favorite removed successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Favorite.DoesNotExist:
            return Response({"success": False, "message": "Favorite not found"}, status=status.HTTP_404_NOT_FOUND)

class ListFavoritesView(generics.ListAPIView):
    serializer_class = getFavoriteSerializer

    def get_queryset(self):
        user_id = self.kwargs['pk']
        return Favorite.objects.filter(user=user_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        if not queryset.exists():
            return Response({
                "success": True,
                "message": "No favorites found",
                "data": []
            }, status=status.HTTP_200_OK)
        return Response({
            "success": True,
            "message": "Favorites retrieved successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)






class RepairingProductStatusUpdateView(APIView):
    def post(self, request, pk):
        try:
            repairing_product = RepairingProduct.objects.get(pk=pk)
        except RepairingProduct.DoesNotExist:
            return Response({'success': False, 'message': 'Repairing product does not exist'}, status=status.HTTP_404_NOT_FOUND)

        current_status = repairing_product.status

        serializer = RepairingProductStatusUpdateSerializer(repairing_product, data=request.data, partial=True)
        if serializer.is_valid():
            new_status = serializer.validated_data.get('status')

            if current_status == 'IN_PROGRESS' and new_status == 'COMPLETED':
                # Update inventory only if the status changes from 'IN_PROGRESS' to 'COMPLETED'
                product_inventory = repairing_product.confirm_booking.booking_request.product_inventory
                product_inventory.need_repairing_quantity -= repairing_product.quantity
                product_inventory.available_quantity += repairing_product.quantity
                product_inventory.save()

            serializer.save()
            return Response({'success': True, 'message': 'Repairing product status updated', 'data': serializer.data}, status=status.HTTP_200_OK)

        return Response({'success': False, 'message': 'Invalid data', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class RepairingProductListView(generics.ListAPIView):
    queryset = RepairingProduct.objects.all()
    serializer_class = RepairingProductSerializer

class ConfirmBookingList(generics.ListAPIView):
    queryset = ConfirmBooking.objects.all()
    serializer_class = ConfirmBookingSerializer

@api_view(['GET'])
def product_inventory_api(request):
    try:
        products = Product.objects.all()
        product_list = []

        for product in products:
            product_data = {
                'id': product.id,
                'category': product.category,
                'image': product.image,
                'name': product.name,
                'quantity': product.quantity,
                'weight': product.weight,
                'size': product.size,
                'pitch': product.pitch,
                'dynamic_attributes': product.dynamic_attributes,
                'inventory': [
                    {
                        'inventory_id': inventory.id,
                        'available_quantity': inventory.available_quantity,
                        'booked_quantity': inventory.booked_quantity,
                        'rental_quantity': inventory.rental_quantity,
                        'damaged_quantity': inventory.damaged_quantity,
                        'need_repairing_quantity': inventory.need_repairing_quantity,
                    } for inventory in product.inventory.all()
                ]
            }
            product_list.append(product_data)

        return Response({
            'success': True,
            'message': 'Product inventory fetched successfully.',
            'data': product_list
        })
    except Exception as e:
        return Response({
            'success': False,
            'message': str(e),
            'data': []
        })
@api_view(['GET'])
def category_list(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        data = {
            'success': True,
            'message': 'Categories retrieved successfully',
            'data': serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

@api_view(['POST'])
def category_create(request):
    if request.method == 'POST':
        serializer = CategorycreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'success': True,
                'message': 'Category created successfully',
                'data': serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        errors = serializer.errors
        if 'name' in errors and 'This category name already exists.' in errors['name']:
            return Response({'success': False, 'message': 'Category name must be unique'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'GET':
        serializer = CategorySerializer(category)
        data = {
            'success': True,
            'message': 'Category retrieved successfully',
            'data': serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'success': True,
                'message': 'Category updated successfully',
                'data': serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        category.delete()
        data = {
            'success': True,
            'message': 'Category deleted successfully'
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)





@api_view(['GET'])
def filter_products_by_category(request, category='all'):
    try:
        print(f"Category received: {category}")  # Debugging statement
        if category and category != "all":
            # Filter products by category
            products = Product.objects.filter(category=category)
            print(f"Filtered products count: {products.count()}")  # Debugging statement
            message = f"Products filtered by category: {category}"
        else:
            # Get all products
            products = Product.objects.all()
            print(f"Total products count: {products.count()}")  # Debugging statement
            message = "All products retrieved"

        # Serialize the queryset
        serializer = ProductFilterSerializer(products, many=True)

        # Return the structured response
        return Response({
            "success": True,
            "message": message,
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    except Exception as e:
        print(f"An error occurred: {e}")  # Debugging statement
        return Response({
            "success": False,
            "message": str(e),
            "data": []
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def update_booking_request_status(request, booking_request_id):
    try:
        booking_request = BookingRequest.objects.get(pk=booking_request_id)
    except BookingRequest.DoesNotExist:
        return Response({'success': False, 'message': 'Booking request does not exist'}, status=status.HTTP_404_NOT_FOUND)

    new_status = request.data.get('status')

    if new_status not in dict(BookingRequest.STATUS_CHOICES):
        return Response({'success': False, 'message': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

    product_inventory = booking_request.product_inventory

    if booking_request.status == 'approved' and new_status != 'approved':
        # Reverse the inventory update for previously approved request
        product_inventory.available_quantity += booking_request.quantity
        product_inventory.booked_quantity -= booking_request.quantity
        product_inventory.save()

        # If there's a ConfirmBooking record, delete it
        ConfirmBooking.objects.filter(booking_request=booking_request).delete()

        booking_request.status = new_status
        booking_request.save()

        return Response({'success': True, 'message': 'Booking request status updated and inventory reversed'}, status=status.HTTP_200_OK)

    if new_status == 'approved':
        # Update status and perform inventory adjustment for approved requests
        booking_request.status = new_status
        booking_request.save()

        # Update product inventory
        product_inventory.available_quantity -= booking_request.quantity
        product_inventory.booked_quantity += booking_request.quantity
        product_inventory.save()

        # Create a confirm booking record
        ConfirmBooking.objects.create(booking_request=booking_request, product=product_inventory.product)

        return Response({'success': True, 'message': 'Booking request approved and inventory updated'}, status=status.HTTP_200_OK)

    # For other statuses, simply update the booking request status
    booking_request.status = new_status
    booking_request.save()

    return Response({'success': True, 'message': 'Booking request status updated'}, status=status.HTTP_200_OK)
@api_view(['POST'])
def create_booking_request(request):
    serializer = BookingRequestSerializer(data=request.data)
    if serializer.is_valid():
        product_inventory = serializer.validated_data.get('product_inventory')
        requested_quantity = serializer.validated_data.get('quantity')

        # Check if the requested quantity is available
        if product_inventory.available_quantity >= requested_quantity:
            # Save the booking request without updating the inventory
            serializer.save()
            return Response({
                'success': True,
                'message': 'Booking request created successfully.',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'success': False,
                'message': 'Insufficient quantity available.',
                'data': {}
            }, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({
            'success': False,
            'message': 'Invalid data.',
            'data': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)








@api_view(['GET'])
def get_all_booking_requests(request):
    try:
        booking_requests = BookingRequest.objects.all()
        serializer = BookingRequestnewSerializer(booking_requests, many=True)
        return Response({
            'success': True,
            'message': 'All booking requests retrieved',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'success': False,
            'message': str(e),
            'data': []
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# @api_view(['GET'])
# def all_bookings_for_user(request, user_id):
#     try:
#         user = User.objects.get(pk=user_id)
#     except User.DoesNotExist:
#         return Response({'success': False, 'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

#     # Retrieve all BookingRequest instances for the specific user
#     booking_requests = BookingRequest.objects.filter(user=user)

#     # Serialize BookingRequest instances
#     serializer = BookingRequestnewSerializer(booking_requests, many=True)
#     data = serializer.data
#     return Response({'success': True, 'message': 'All bookings retrieved successfully', 'data': data}, status=status.HTTP_200_OK)

@api_view(['GET'])
def all_bookings_for_user(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'success': False, 'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

    # Retrieve all BookingRequest instances for the specific user
    booking_requests = BookingRequest.objects.filter(user=user)

    if not booking_requests.exists():
        return Response({'success': False, 'message': 'No booking requests found for this user'}, status=status.HTTP_200_OK)

    # Serialize BookingRequest instances
    serializer = BookingRequestnewSerializer(booking_requests, many=True)
    data = serializer.data

    return Response({'success': True, 'message': 'All bookings retrieved successfully', 'data': data}, status=status.HTTP_200_OK)


@api_view(['POST'])
def update_confirm_booking_status(request, confirm_booking_id):
    try:
        confirm_booking = ConfirmBooking.objects.get(pk=confirm_booking_id)
    except ConfirmBooking.DoesNotExist:
        return Response({'success': False, 'message': 'Confirm booking does not exist'}, status=status.HTTP_404_NOT_FOUND)

    # Check if the current status is already "BORROWED"
    if confirm_booking.status == 'BORROWED':
        return Response({'success': True, 'message': 'Confirm booking is already in BORROWED status'}, status=status.HTTP_200_OK)

    # Update product inventory quantities for BORROWED status
    product_inventory = confirm_booking.booking_request.product_inventory
    product_inventory.booked_quantity -= confirm_booking.booking_request.quantity
    product_inventory.rental_quantity += confirm_booking.booking_request.quantity
    product_inventory.save()

    # Update the status to BORROWED
    confirm_booking.status = 'BORROWED'
    confirm_booking.save()

    return Response({'success': True, 'message': 'booking product hass been recieved by the user'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def update_confirm_booking_status_to_returned(request, confirm_booking_id):
    try:
        confirm_booking = ConfirmBooking.objects.get(pk=confirm_booking_id)
    except ConfirmBooking.DoesNotExist:
        return Response({'success': False, 'message': 'Confirm booking does not exist'}, status=status.HTTP_404_NOT_FOUND)

    # Check if the current status is already "RETURNED"
    if confirm_booking.status == 'RETURNED':
        return Response({'success': True, 'message': 'Confirm booking is already in RETURNED status'}, status=status.HTTP_200_OK)

    # Get damage_quantity, repairing_quantity, and return_quantity from request data
    damage_quantity = request.data.get('damage_quantity', 0)
    repairing_quantity = request.data.get('repairing_quantity', 0)
    return_quantity = request.data.get('return_quantity', 0)

    # Validate the data
    if damage_quantity < 0 or repairing_quantity < 0 or return_quantity < 0:
        return Response({'success': False, 'message': 'Damage quantity, repairing quantity, and return quantity must be non-negative'}, status=status.HTTP_400_BAD_REQUEST)

    # Calculate the total quantity returned
    total_returned_quantity = damage_quantity + repairing_quantity + return_quantity

    # Ensure the total returned quantity matches the quantity borrowed
    if total_returned_quantity != confirm_booking.booking_request.quantity:
        return Response({'success': False, 'message': 'Total returned quantity does not match the quantity borrowed'}, status=status.HTTP_400_BAD_REQUEST)

    # Update the status to RETURNED
    confirm_booking.status = 'RETURNED'
    confirm_booking.save()

    # Update product inventory quantities
    product_inventory = confirm_booking.booking_request.product_inventory

    # Manage damaged_quantity, need_repairing_quantity, and rental_quantity
    product_inventory.damaged_quantity += damage_quantity
    product_inventory.need_repairing_quantity += repairing_quantity
    product_inventory.rental_quantity -= total_returned_quantity

    if return_quantity > 0:
        product_inventory.available_quantity += return_quantity

    product_inventory.save()

    # Create instances of DamagedProduct if there are damaged quantities
    if damage_quantity > 0:
        DamagedProduct.objects.create(confirm_booking=confirm_booking, quantity=damage_quantity)

    # Create instances of RepairingProduct if there are repairing quantities
    if repairing_quantity > 0:
        RepairingProduct.objects.create(confirm_booking=confirm_booking, quantity=repairing_quantity)

    return Response({'success': True, 'message': 'Confirm booking status updated to RETURNED'}, status=status.HTTP_200_OK)








@csrf_exempt
@api_view(['POST'])
def upload_numbers_file(request):
    if 'numbers_file' not in request.FILES:
        return Response({"error": "No file was submitted."}, status=status.HTTP_400_BAD_REQUEST)

    numbers_file = request.FILES['numbers_file']

    # Check if the uploaded file has .numbers extension
    if not numbers_file.name.endswith('.numbers'):
        return Response({"error": "Invalid file format. Please upload a .numbers file."}, status=status.HTTP_400_BAD_REQUEST)

    # Check if category is provided
    category_name = request.data.get('category', None)
    print("Category Name:", category_name)  # Debug print for category name
    if not category_name:
        return Response({"error": "Category is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Save the uploaded file to a temporary location
        temp_file_path = numbers_file.temporary_file_path()
        print("Temporary file path:", temp_file_path)

        # Parse the .numbers file using the temporary file path
        doc = Document(temp_file_path)
        sheets = doc.sheets
        print("Sheets type:", type(sheets))
        print("Number of sheets:", len(sheets))

        # Prepare to store the table data in JSON format
        json_data = {}

        # Process the data
        for sheet_index, sheet in enumerate(sheets):
            print("Processing sheet", sheet_index + 1, ":")
            print("Sheet name:", sheet.name)
            print("Tables type:", type(sheet.tables))
            print("Number of tables:", len(sheet.tables))

            sheet_data = {}
            for table_index, table in enumerate(sheet.tables):
                print("Processing table", table_index + 1, ":")
                print("Table type:", type(table))

                table_data = []
                try:
                    print("Table content:")
                    for row_index, row in enumerate(table.rows()):
                        row_data = [cell.value for cell in row]
                        print(f"Row {row_index + 1}: {row_data}")
                        table_data.append(row_data)
                except Exception as e:
                    print(f"An error occurred while processing table rows: {e}")
                sheet_data[f"Table_{table_index + 1}"] = table_data

            json_data[f"Sheet_{sheet_index + 1}"] = sheet_data

        # Process data rows (skip the header row)
        for sheet_key, sheet in json_data.items():
            for table_key, table in sheet.items():
                header_row = table[0]  # Header row
                data_rows = table[1:]  # Data rows

                for row in data_rows:
                    row_data = {header_row[i]: value for i, value in enumerate(row)}

                    # Convert Duration objects to string format before passing to the serializer
                    for key, value in row_data.items():
                        if isinstance(value, timedelta):
                            row_data[key] = str(value)

                    # Extract relevant fields from row_data and map to product_data
                    product_data = {
                        'image': row_data.get('Image', '') or '/productimages/default.png',
                        'name': row_data.get('Name(Model)', ''),
                        'quantity': row_data.get('Quantity', ''),
                        'weight': row_data.get('Weight(Kg)', ''),
                        'size': row_data.get('Size(mm)', ''),
                        'pitch': row_data.get('Pitch', ''),
                        'dynamic_attributes': {key: row_data[key] for key in row_data if key not in ['Image', 'Name(Model)', 'Quantity', 'Weight(Kg)', 'Size(mm)', 'Pitch']},
                        'category': category_name  # Assign category name directly
                    }
                    print("Product Data:", product_data)  # Debug print for product data

                    # Check if product with same name exists
                    product = Product.objects.filter(name=product_data['name']).first()
                    if product:
                        # Update existing product
                        serializer = ProductSerializer(product, data=product_data, partial=True)
                    else:
                        # Create new product
                        serializer = ProductSerializer(data=product_data)

                    if serializer.is_valid():
                        product = serializer.save()

                        # Extract and convert quantity
                        quantity_str = row_data.get('Quantity', '0')
                        match = re.search(r'\d+', quantity_str)
                        quantity = int(match.group()) if match else 0

                        # Get or create the inventory record
                        inventory, created = ProductInventory.objects.get_or_create(product=product)
                        inventory.available_quantity += quantity
                        inventory.save()
                    else:
                        print("Validation errors:", serializer.errors)
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        print("File processed successfully")
        return Response({"message": "File processed successfully"}, status=status.HTTP_201_CREATED)

    except Exception as e:
        print("An error occurred:", str(e))
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# @csrf_exempt


# @api_view(['POST'])
# def upload_numbers_file(request):
#     if 'numbers_file' not in request.FILES:
#         return Response({"error": "No file was submitted."}, status=status.HTTP_400_BAD_REQUEST)

#     numbers_file = request.FILES['numbers_file']

#     # Check if the uploaded file has .numbers extension
#     if not numbers_file.name.endswith('.numbers'):
#         return Response({"error": "Invalid file format. Please upload a .numbers file."}, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         # Save the uploaded file to a temporary location
#         temp_file_path = numbers_file.temporary_file_path()
#         print("Temporary file path:", temp_file_path)

#         # Parse the .numbers file using the temporary file path
#         doc = Document(temp_file_path)
#         sheets = doc.sheets
#         print("Sheets type:", type(sheets))
#         print("Number of sheets:", len(sheets))

#         # Prepare to store the table data in JSON format
#         json_data = {}

#         # Process the data
#         for sheet_index, sheet in enumerate(sheets):
#             print("Processing sheet", sheet_index + 1, ":")
#             print("Sheet name:", sheet.name)
#             print("Tables type:", type(sheet.tables))
#             print("Number of tables:", len(sheet.tables))

#             sheet_data = {}
#             for table_index, table in enumerate(sheet.tables):
#                 print("Processing table", table_index + 1, ":")
#                 print("Table type:", type(table))

#                 table_data = []
#                 try:
#                     print("Table content:")
#                     for row_index, row in enumerate(table.rows()):
#                         row_data = [cell.value for cell in row]
#                         print(f"Row {row_index + 1}: {row_data}")
#                         table_data.append(row_data)
#                 except Exception as e:
#                     print(f"An error occurred while processing table rows: {e}")
#                 sheet_data[f"Table_{table_index + 1}"] = table_data

#             json_data[f"Sheet_{sheet_index + 1}"] = sheet_data

#         # Process data rows (skip the header row)
#         for sheet_key, sheet in json_data.items():
#             for table_key, table in sheet.items():
#                 header_row = table[0]  # Header row
#                 data_rows = table[1:]  # Data rows

#                 for row in data_rows:
#                     row_data = {header_row[i]: value for i, value in enumerate(row)}

#                     # Convert Duration objects to string format before passing to the serializer
#                     for key, value in row_data.items():
#                         if isinstance(value, timedelta):
#                             row_data[key] = str(value)

#                     # Extract relevant fields from row_data and map to product_data
#                     product_data = {
#                         'image': row_data.get('Image', '') or '',
#                         'name': row_data.get('Name(Model)', ''),
#                         'quantity': row_data.get('Quantity', ''),
#                         'weight': row_data.get('Weight(Kg)', ''),
#                         'size': row_data.get('Size(mm)', ''),
#                         'pitch': row_data.get('Pitch', ''),
#                         'dynamic_attributes': {key: row_data[key] for key in row_data if key not in ['Image', 'Name(Model)', 'Quantity', 'Weight(Kg)', 'Size(mm)', 'Pitch']}
#                     }

#                     # Check if product with same name exists
#                     product = Product.objects.filter(name=product_data['name']).first()
#                     if product:
#                         # Update existing product
#                         serializer = ProductSerializer(product, data=product_data, partial=True)
#                     else:
#                         # Create new product
#                         serializer = ProductSerializer(data=product_data)

#                     if serializer.is_valid():
#                         product = serializer.save()

#                         # Extract and convert quantity
#                         quantity_str = row_data.get('Quantity', '0')
#                         match = re.search(r'\d+', quantity_str)
#                         quantity = int(match.group()) if match else 0

#                         # Get or create the inventory record
#                         inventory, created = ProductInventory.objects.get_or_create(product=product)
#                         inventory.available_quantity += quantity
#                         inventory.save()
#                     else:
#                         print("Validation errors:", serializer.errors)
#                         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         print("File processed successfully")
#         return Response({"message": "File processed successfully"}, status=status.HTTP_201_CREATED)

#     except Exception as e:
#         print("An error occurred:", str(e))
#         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# @api_view(['POST'])
# def upload_numbers_file(request):
#     if 'numbers_file' not in request.FILES:
#         return Response({"error": "No file was submitted."}, status=status.HTTP_400_BAD_REQUEST)

#     numbers_file = request.FILES['numbers_file']

#     # Check if the uploaded file has .numbers extension
#     if not numbers_file.name.endswith('.numbers'):
#         return Response({"error": "Invalid file format. Please upload a .numbers file."}, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         # Save the uploaded file to a temporary location
#         temp_file_path = numbers_file.temporary_file_path()
#         print("Temporary file path:", temp_file_path)

#         # Parse the .numbers file using the temporary file path
#         doc = Document(temp_file_path)
#         sheets = doc.sheets
#         print("Sheets type:", type(sheets))
#         print("Number of sheets:", len(sheets))

#         # Prepare to store the table data in JSON format
#         json_data = {}

#         # Process the data
#         for sheet_index, sheet in enumerate(sheets):
#             print("Processing sheet", sheet_index + 1, ":")
#             print("Sheet name:", sheet.name)
#             print("Tables type:", type(sheet.tables))
#             print("Number of tables:", len(sheet.tables))

#             sheet_data = {}
#             for table_index, table in enumerate(sheet.tables):
#                 print("Processing table", table_index + 1, ":")
#                 print("Table type:", type(table))

#                 table_data = []
#                 try:
#                     print("Table content:")
#                     for row_index, row in enumerate(table.rows()):
#                         row_data = [cell.value for cell in row]
#                         print(f"Row {row_index + 1}: {row_data}")
#                         table_data.append(row_data)
#                 except Exception as e:
#                     print(f"An error occurred while processing table rows: {e}")
#                 sheet_data[f"Table_{table_index + 1}"] = table_data

#             json_data[f"Sheet_{sheet_index + 1}"] = sheet_data

#         # Process data rows (skip the header row)
#         for sheet_key, sheet in json_data.items():
#             for table_key, table in sheet.items():
#                 header_row = table[0]  # Header row
#                 data_rows = table[1:]  # Data rows

#                 for row in data_rows:
#                     row_data = {header_row[i]: value for i, value in enumerate(row)}

#                     # Convert Duration objects to string format before passing to the serializer
#                     for key, value in row_data.items():
#                         if isinstance(value, timedelta):
#                             row_data[key] = str(value)

#                     # Extract relevant fields from row_data and map to product_data
#                     product_data = {
#                         'image': row_data.get('Image', '') or '',
#                         'name': row_data.get('Name(Model)', ''),
#                         'quantity': row_data.get('Quantity', ''),
#                         'weight': row_data.get('Weight(Kg)', ''),
#                         'size': row_data.get('Size(mm)', ''),
#                         'pitch': row_data.get('Pitch', ''),
#                         'dynamic_attributes': {key: row_data[key] for key in row_data if key not in ['Image', 'Name(Model)', 'Quantity', 'Weight(Kg)', 'Size(mm)', 'Pitch']}
#                     }

#                     # Validate and save the product data
#                     serializer = ProductSerializer(data=product_data)
#                     if serializer.is_valid():
#                         serializer.save()
#                     else:
#                         print("Validation errors:", serializer.errors)
#                         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         print("File processed successfully")
#         return Response({"message": "File processed successfully"}, status=status.HTTP_201_CREATED)

#     except Exception as e:
#         print("An error occurred:", str(e))
#         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# @api_view(['POST'])
# def upload_numbers_file(request):
#     if 'numbers_file' not in request.FILES:
#         return Response({"error": "No file was submitted."}, status=status.HTTP_400_BAD_REQUEST)

#     numbers_file = request.FILES['numbers_file']

#     # Check if the uploaded file has .numbers extension
#     if not numbers_file.name.endswith('.numbers'):
#         return Response({"error": "Invalid file format. Please upload a .numbers file."}, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         # Save the uploaded file to a temporary location
#         temp_file_path = numbers_file.temporary_file_path()
#         print("Temporary file path:", temp_file_path)

#         # Parse the .numbers file using the temporary file path
#         doc = Document(temp_file_path)
#         sheets = doc.sheets
#         print("Sheets type:", type(sheets))
#         print("Number of sheets:", len(sheets))

#         # Prepare to store the table data in JSON format
#         json_data = {}

#         # Process the data
#         for sheet_index, sheet in enumerate(sheets):
#             print("Processing sheet", sheet_index + 1, ":")
#             print("Sheet name:", sheet.name)
#             print("Tables type:", type(sheet.tables))
#             print("Number of tables:", len(sheet.tables))

#             sheet_data = {}
#             for table_index, table in enumerate(sheet.tables):
#                 print("Processing table", table_index + 1, ":")
#                 print("Table type:", type(table))

#                 table_data = []
#                 try:
#                     print("Table content:")
#                     for row_index, row in enumerate(table.rows()):
#                         row_data = [cell.value for cell in row]
#                         print(f"Row {row_index + 1}: {row_data}")
#                         table_data.append(row_data)
#                 except Exception as e:
#                     print(f"An error occurred while processing table rows: {e}")
#                 sheet_data[f"Table_{table_index + 1}"] = table_data

#             json_data[f"Sheet_{sheet_index + 1}"] = sheet_data

#         # Process each row and save it as product data
#         for sheet_key, sheet in json_data.items():
#             for table_key, table in sheet.items():
#                 for row in table:
#                     row_data = {f"Column_{i + 1}": value for i, value in enumerate(row)}

#                     # Convert Duration objects to string format before passing to the serializer
#                     for key, value in row_data.items():
#                         if isinstance(value, timedelta):
#                             row_data[key] = str(value)

#                     # Extract relevant fields from row_data and map to product_data
#                     product_data = {
#                         'image': row_data.get('Column_1', '') or '',
#                         'name': row_data.get('Column_2', ''),
#                         'quantity': row_data.get('Column_3', ''),
#                         'weight': row_data.get('Column_4', ''),
#                         'size': row_data.get('Column_5', ''),
#                         'pitch': row_data.get('Column_6', ''),
#                         'dynamic_attributes': {key: row_data[key] for key in row_data if key not in ['Column_1', 'Column_2', 'Column_3', 'Column_4', 'Column_5', 'Column_6']}
#                     }

#                     # Validate and save the product data
#                     serializer = ProductSerializer(data=product_data)
#                     if serializer.is_valid():
#                         serializer.save()
#                     else:
#                         print("Validation errors:", serializer.errors)
#                         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         print("File processed successfully")
#         return Response({"message": "File processed successfully"}, status=status.HTTP_201_CREATED)

#     except Exception as e:
#         print("An error occurred:", str(e))
#         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class CSVUploadView(APIView):
    def post(self, request, *args, **kwargs):
        csv_file = request.FILES.get('file')
        if not csv_file:
            return Response({"error": "No file was submitted."}, status=status.HTTP_400_BAD_REQUEST)

        if not csv_file.name.endswith('.csv'):
            return Response({"error": "Please upload a valid CSV file."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            file_data = csv_file.read().decode("utf-8")
            lines = file_data.split("\n")
            reader = csv.DictReader(lines)

            print("Processing CSV file...")

            if not reader:
                print("No rows found in the CSV file")
                return Response({"error": "No rows found in the CSV file"}, status=status.HTTP_400_BAD_REQUEST)

            for row in reader:
                print("Processing row:", row)


                # Extract numeric part from quantity string using regular expression


                product_data = {
                    'image': row.get('Image', ''),
                    'name': row.get('Name(Model)', ''),
                    'quantity': row.get('Quantity', ''),
                    'weight': row.get('Weight(Kg)', ''),
                    'size': row.get('Size(mm)', ''),
                    'pitch': row.get('Pitch', ''),
                    'dynamic_attributes': {key: row[key] for key in row if key not in ['Image', 'Name(Model)', 'Quantity', 'Weight(Kg)', 'Size(mm)', 'Pitch']}
                }

                # Validate and save the product data
                serializer = ProductSerializer(data=product_data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    # Return validation errors if any
                    print("Validation errors:", serializer.errors)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            print("CSV file processed successfully")
            return Response({"message": "CSV file processed successfully"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            print("An error occurred:", str(e))
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class ProductListView(APIView):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




















