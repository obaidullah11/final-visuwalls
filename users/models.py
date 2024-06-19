from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, AbstractUser
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import uuid
from django.utils.crypto import get_random_string

from django.contrib.auth.base_user import BaseUserManager

class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, user_type='client', **extra_fields):
        """
        Creates and saves a User with the given email, username, password, and optional extra fields.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            user_type=user_type,
            **extra_fields
        )

        if password:
            user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, user_type='super_admin', **extra_fields):
        """
        Creates and saves a superuser with the given email, username, password, and optional extra fields.
        """
        user = self.create_user(
            email=email,
            username=username,
            password=password,
            user_type=user_type,
            **extra_fields
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
class CustomUserIDField(models.CharField):
    def pre_save(self, model_instance, add):
        # Generate a 6-digit ID if it's a new instance
        if add:
            return get_random_string(length=6, allowed_chars='0123456789')
        else:
            return super().pre_save(model_instance, add)
# Create your models here.
class User(AbstractUser):
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    id = CustomUserIDField(primary_key=True, max_length=6, editable=False)
    USER_TYPE_CHOICES = (
    ('client', 'client'),
    ('supplier', 'supplier'),
    ('super_admin', 'Super Admin'),

    )
    device_token = models.CharField(max_length=255, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    is_registered = models.BooleanField(default=False)

    verify = models.BooleanField(default=False)
    otp_code = models.CharField(max_length=6, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    username=models.CharField(max_length=200)
    user_type = models.CharField(
        max_length=255, default='client', choices=USER_TYPE_CHOICES)
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='user_images/', null=True, blank=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['contact','name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    class Meta:
        # Add any other meta options if needed
        verbose_name = "User"
        verbose_name_plural = "User"


class Company(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name