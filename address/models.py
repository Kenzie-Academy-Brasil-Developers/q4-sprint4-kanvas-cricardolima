from uuid import uuid4

from django.db import models

class Address(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    street = models.CharField(max_length=255)
    house_number = models.IntegerField()
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)
    country = models.CharField(max_length=255)