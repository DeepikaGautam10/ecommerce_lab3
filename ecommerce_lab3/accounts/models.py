from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('business', 'Business Owner'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='customer')
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.username

class Role(models.Model):
    ROLE_CHOICES = (
        ('viewer', 'Viewer'),
        ('accountant', 'Accountant'),
        ('admin', 'Admin'),
    )
    name = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)
    description = models.TextField()
    
    def __str__(self):
        return self.get_name_display()

class Permission(models.Model):
    name = models.CharField(max_length=100, unique=True)
    codename = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    
    def __str__(self):
        return self.name

class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permissions = models.ManyToManyField(Permission, blank=True)
    assigned_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'role')
    
    def __str__(self):
        return f"{self.user.username} - {self.role.name}"