from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Notification
# Create your views here.
from .serializers import NotificationSerializer


from rest_framework.response import Response
from rest_framework import status
from firebase_admin import messaging
from users.models import User  # Make sure to adjust this import if your User model is different
# from firebase_admin import messaging
from firebase_admin.exceptions import FirebaseError





@api_view(['POST'])
def update_notification_status(request, notification_id):
    try:
        # Retrieve the notification object
        notification = Notification.objects.get(pk=notification_id)

        # Update notification status (e.g., mark as seen)
        notification.seen = True  # Update the status as needed based on request data
        notification.save()  # Save the updated notification object

        # Serialize the updated notification
        serializer = NotificationSerializer(notification)

        # Prepare response data
        data = {
            'success': True,
            'message': 'Notification status updated successfully',
            'data': serializer.data
        }

        return Response(data, status=status.HTTP_200_OK)

    except Notification.DoesNotExist:
        data = {
            'success': False,
            'error': 'Notification not found'
        }
        return Response(data, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        data = {
            'success': False,
            'error': str(e)
        }
        return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_user_notifications(request, user_id):
    try:
        # Retrieve the user object
        user = User.objects.get(pk=user_id)

        # Retrieve all notifications for the user
        notifications = Notification.objects.filter(user=user)

        # Serialize the notifications
        serializer = NotificationSerializer(notifications, many=True)

        # Prepare response data
        data = {
            'success': True,
            'message': 'Notifications retrieved successfully',
            'data': serializer.data
        }

        return Response(data, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        data = {
            'success': False,
            'error': 'User not found'
        }
        return Response(data, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        data = {
            'success': False,
            'error': str(e)
        }
        return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)









# Get an instance of a logger
@api_view(['POST'])
def send_notification_to_all_users(request):
    try:
        title = request.data.get('title')
        body = request.data.get('body')

        print(f"Received data: title={title}, body={body}")

        if not title or not body:
            print("Missing required data: title or body")
            return Response({'error': 'title and body are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve all users
        users = User.objects.all()

        # Iterate over each user and send notification
        for user in users:
            device_token = user.device_token

            if not device_token:
                print(f"User {user.id} has no device token, skipping...")
                continue

            # Construct the FCM message
            message = messaging.Message(
                notification=messaging.Notification(title=title, body=body),
                token=device_token,
            )

            # Send the FCM message
            response = messaging.send(message)
            data = {'recipient_id': user.id, 'response': str(response)}

            # Create a notification record
            notification = Notification.objects.create(
                user=user,
                title=title,
                message=body,
                seen=False  # Assuming the notification is initially unseen
            )

            print(f"Notification sent to user_id: {user.id} with response: {response}")

        return Response({'success': True, 'message': 'Notifications sent successfully'}, status=status.HTTP_200_OK)

    except Exception as e:
        print(f"Error sending notifications: {str(e)}")
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@api_view(['POST'])
def send_notification_to_user(request):
    try:
        user_id = request.data.get('user_id')
        title = request.data.get('title')
        body = request.data.get('body')

        print(f"Received data: user_id={user_id}, title={title}, body={body}")

        if not user_id or not title or not body:
            print("Missing required data: user_id, title, or body")
            return Response({'error': 'user_id, title, and body are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the recipient user
        recipient = User.objects.get(pk=user_id)

        # Retrieve the device_token directly from the recipient (User) object
        device_token = recipient.device_token

        if not device_token:
            print("Recipient has no device token")
            return Response({'success': False, 'message': 'Recipient has no device token'}, status=status.HTTP_400_BAD_REQUEST)

        # Construct the FCM message
        message = messaging.Message(
            notification=messaging.Notification(title=title, body=body),
            token=device_token,
        )

        # Send the FCM message
        response = messaging.send(message)
        data = {'recipient_id': user_id, 'response': str(response)}

        # Create a notification record
        notification = Notification.objects.create(
            user=recipient,
            title=title,
            message=body,
            seen=False  # Assuming the notification is initially unseen
        )

        print(f"Notification record created for user_id: {user_id}")

        return Response({'success': True, 'message': 'Notification sent successfully', 'data': data}, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        print(f"Recipient not found for user_id: {user_id}")
        return Response({'success': False, 'error': 'Recipient not found'}, status=status.HTTP_404_NOT_FOUND)

    except FirebaseError as e:
        error_message = str(e)
        if "SenderId mismatch" in error_message:
            error_message = "SenderId mismatch"
        print(f"Error sending notification: {error_message}")
        return Response({'success': False, 'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        error_message = f"Error sending notification: {str(e)}"
        print(error_message)
        return Response({'success': False, 'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)