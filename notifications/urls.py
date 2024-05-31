from django.urls import path
from .views import *

urlpatterns = [


    path('api/send_notification/', send_notification_to_user, name='send_notification_to_user'),


    path('api/getusernotifications/<int:user_id>/', get_user_notifications, name='user_notifications'),
    path('api/notifications_update/<int:notification_id>/', update_notification_status, name='update_notification_status'),
    path('api/send-notification-to-all-users/', send_notification_to_all_users, name='send_notification_to_all_users'),


    # path('api/host_car_details/<int:pk>/update-image/', HostCarDetailsImageUpdateAPIView.as_view(), name='update_car_image'),
    # path('trip-booking/create/', TripBookingCreateAPIView.as_view(), name='trip-booking-create'),

]
