from django.db import models

# Create your models here.
# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    USER_TYPES = (
        ('admin', 'Admin'),
        ('user', 'User'),
        ('viewer', 'Viewer'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='viewer')

class Customer(models.Model):
    business_name = models.CharField(max_length=200)
    contact_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customers_created')

    def __str__(self):
        return self.business_name

    class Meta:
        ordering = ['-created_at']

class Comment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.customer.business_name}"

    class Meta:
        ordering = ['-created_at']