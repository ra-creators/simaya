# Generated by Django 3.2.10 on 2022-01-27 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraddress',
            name='address_type',
            field=models.CharField(choices=[('Home', 'Home'), ('Work', 'Work')], default='Home', max_length=20),
        ),
    ]