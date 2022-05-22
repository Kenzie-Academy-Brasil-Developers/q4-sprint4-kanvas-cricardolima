from django.db import models
from django.contrib.auth.models import AbstractUser

from uuid import uuid4

class User(AbstractUser):
    uuid = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    is_admin = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, null=True, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    address = models.ForeignKey('address.Address', on_delete=models.CASCADE, related_name='users', null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []