# Generated by Django 4.0.4 on 2022-05-29 15:52

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('phone', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='phone_number',
            new_name='PhoneNumber',
        ),
    ]
