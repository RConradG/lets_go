# Generated by Django 5.2 on 2025-05-06 10:44

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_alter_event_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testmodel',
            name='image',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='image'),
        ),
    ]
