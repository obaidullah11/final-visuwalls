from django.urls import path
from users.views import ResendOTPView,set_new_password,CompanyCheckAPIView,CompanyCreateAPIView,SendPasswordResetEmailView,VerifyOTP,list_users,UserUpdateAPIView, UserChangePasswordView, UserLoginView, UserProfileView, UserRegistrationView,UserDeleteAPIView, UserPasswordResetView
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('me/', UserProfileView.as_view(), name='profile'),
    path('changepassword/<str:custom_id>/', UserChangePasswordView.as_view(), name='change-password'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    path('account/activation/', VerifyOTP.as_view(), name='verify_otp'),
    path('updateProfile/<str:custom_id>/', UserUpdateAPIView.as_view(), name='user-update'),
    path('delete/<str:custom_id>/', UserDeleteAPIView.as_view(), name='user-delete'),
    path('getallusers/', list_users, name='list_users'),
    path('create/companies/', CompanyCreateAPIView.as_view(), name='company-create'),
    path('company/check/', CompanyCheckAPIView.as_view(), name='company-check'),
    path('forgotpassword/', set_new_password, name='set_new_password'),
    path('resend_otp/', ResendOTPView.as_view(), name='resend_otp'),

    # path('getallusers/', list_users, name='list_users'),

]