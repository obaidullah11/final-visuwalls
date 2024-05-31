from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User,Company

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ( 'user_type', 'image', 'device_token','address')}),
        ('Permissions', {'fields': ('is_active',  'is_superuser')}),
        ('Important dates', {'fields': ('last_login',  )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email',  'user_type', 'password1', 'password2'),
        }),
    )
    list_display = ('id','username','otp_code','verify', 'email', 'user_type', 'is_active', 'is_staff', 'is_superuser','first_name', 'last_name', 'address')
    list_filter = ('user_type', 'is_active',  'is_superuser')
    search_fields = ('username', 'email')
    ordering = ('username',)

admin.site.register(User, UserAdmin)
admin.site.register(Company)