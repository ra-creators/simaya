# Generated by Django 3.2.10 on 2022-01-30 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20220127_2011'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='diamond',
            field=models.CharField(default='a', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderitem',
            name='metal',
            field=models.CharField(default='a', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderitem',
            name='size',
            field=models.CharField(default='a', max_length=5),
            preserve_default=False,
        ),
    ]