# Generated by Django 4.2.3 on 2023-09-30 12:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0005_remove_product_is_favorite_remove_product_is_in_cart_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]