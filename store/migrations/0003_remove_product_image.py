# Generated by Django 4.2.3 on 2023-07-29 00:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_product_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
    ]
