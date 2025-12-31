from django.db import models
from users.models import User
import uuid

# Create your models here.
class GeneralInfo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # site_name = models.CharField(max_length=10)
    # site_logo = models.ImageField()
    location = models.CharField(max_length=255, default='Port Harcourt, Nigeria')
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, default='+2348074259720')
    head_office_email = models.EmailField(null=True)
    head_office_phone_number = models.CharField(max_length=15, default='+2348074259720')
    support_office_email = models.EmailField(null=True)
    support_office_phone_number = models.CharField(max_length=15, default='+2348074259720')
    sales_office_email = models.EmailField(null=True)
    sales_office_phone_number = models.CharField(max_length=15, default='+2348074259720')
    purchase_office_email = models.EmailField(null=True)
    purchase_office_phone_number = models.CharField(max_length=15, default='+2348074259720')
    linkedIn_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    telegram_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.email
    
    def get_social_links(self):
        return {
            "linkedin_url": self.linkedIn_url,
            "github_url": self.github_url,
            "instagram_url": self.instagram_url,
            "twitter_url": self.twitter_url,
            "telegram_url": self.telegram_url,
            "facebook_url": self.facebook_url,
        }

class HeroSection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True)
    button_text = models.CharField(max_length=50, default="EXPLORE NOW")
    button_link = models.URLField(blank=True)
    image = models.ImageField(upload_to='hero/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class HomepageSection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=150)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='homepage/')
    button_text = models.CharField(max_length=50, default="Shop Now")
    button_link = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

