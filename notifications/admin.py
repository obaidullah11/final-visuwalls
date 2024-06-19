from django.contrib import admin
from .models import Notification
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'seen', 'created_at')
    list_filter = ('seen', 'created_at')
    search_fields = ('title', 'message', 'user__username')

