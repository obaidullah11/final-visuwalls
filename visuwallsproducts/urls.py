from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import *

urlpatterns = [
    path('api/import_numbers/', upload_numbers_file, name='upload-csv'),
    path('api/getallproducts/', ProductListView.as_view(), name='product-list'),
    path('api/requestbooking/', create_booking_request, name='product-list'),
    path('api/updatebooking/', update_booking_request_status, name='update-booking'),
    path('api/productsfilter/<str:category>/', filter_products_by_category, name='filter_products_by_category'),
    path('api/categories/', category_list, name='category-list'),
    path('api/categories/<int:pk>/', category_detail, name='category-detail'),
    path('api/categories/create/',category_create, name='category-create'),
    path('api/create_booking_request/', create_booking_request, name='create_booking_request'),
    path('api/update_booking_request_status/<int:booking_request_id>/',update_booking_request_status, name='update_booking_request_status'),
    path('api/getallbookingrequests/', get_all_booking_requests, name='get_all_booking_requests'),
    path('api/bookingstatus/<int:user_id>/', all_bookings_for_user, name='confirm_bookings_for_user'),
    path('api/getdetailproduct/', product_inventory_api, name='product-list-create'),
    path('api/confirm-bookings/', ConfirmBookingList.as_view(), name='confirm-booking-list'),
    path('api/dispatchproducttoclient/<int:confirm_booking_id>/', update_confirm_booking_status, name='update_confirm_booking_status'),
    path('api/returnborowedproduct/<int:confirm_booking_id>/', update_confirm_booking_status_to_returned, name='update_confirm_booking_status_to_returned'),
    path('api/repairing_products/', RepairingProductListView.as_view(), name='repairing-product-list'),
    path('api/repairing_products/<int:pk>/', RepairingProductStatusUpdateView.as_view(), name='repairing-product-update-status'),
    path('api/favorites/', AddFavoriteView.as_view(), name='add_favorite'),
    path('api/remove_favorite/<int:favorite_id>/', RemoveFavoriteView.as_view(), name='remove_favorite'),
    path('api/favorites/list/<int:pk>/', ListFavoritesView.as_view(), name='list_favorites'),
    path('api/search_product/', search_product, name='search_product'),


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
