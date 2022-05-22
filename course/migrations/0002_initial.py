# Generated by Django 4.0.4 on 2022-05-22 22:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses',
            name='instructor',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='instructor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='courses',
            name='students',
            field=models.ManyToManyField(related_name='students', to=settings.AUTH_USER_MODEL),
        ),
    ]
