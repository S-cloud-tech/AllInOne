from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid
# from django_countries import Countries
import random
from datetime import timedelta

# Create your models here.
class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('merchant', 'Merchant'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    tax_number = models.CharField(max_length=100, blank=True, null=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='customer')
    is_merchant = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.email} ({self.user_type})"


class EmailOTP(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    creat_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    @staticmethod
    def generate_otp():
        return str(random.randint(100000,999999))
    
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    @classmethod
    def create_for_user(cls, user):
        otp = cls.generate_otp()
        expires_at = timezone.now() + timedelta(minutes=10)
        instance = cls.objects.create(user=user, otp=otp, expires_at=expires_at)
        return instance
    
    @classmethod
    def can_resend(cls, user):
        """Allow resend only every 2 minutes"""
        recent = cls.objects.filter(user=user).order_by('-created_at').first()
        if recent and timezone.now() - recent.created_at < timedelta(minutes=2):
            return False
        return True

    @classmethod
    def remaining_cooldown(cls, user):
        """Return seconds remaining before resend allowed"""
        recent = cls.objects.filter(user=user).order_by('-created_at').first()
        if recent:
            diff = timezone.now() - recent.created_at
            remaining = 120 - diff.total_seconds()  # 2 minutes = 120 sec
            return max(0, int(remaining))
        return 0

class PasswordResetOTP(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.otp}"

    @staticmethod
    def generate_otp():
        return str(random.randint(100000, 999999))
