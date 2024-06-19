from rest_framework import serializers
from .models import Notification
from users.serializers import UserProfileSerializer
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'title', 'message', 'seen', 'created_at']