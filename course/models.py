from uuid import uuid4

from django.db import models

class Courses(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=255, unique=True)
    demo_time = models.TimeField()
    created_at = models.DateField(auto_now_add=True)
    link_repo = models.CharField(max_length=255)
    instructor = models.OneToOneField('user.User', on_delete=models.CASCADE, related_name='instructor', null=True)
    students = models.ManyToManyField('user.User', related_name='students')