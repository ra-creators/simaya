# Generated by Django 3.2.10 on 2022-01-29 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_manager', '0002_useraddress_address_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
