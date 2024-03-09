# Generated by Django 4.2.3 on 2023-09-30 12:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0004_customuser_cart_products_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='is_favorite',
        ),
        migrations.RemoveField(
            model_name='product',
            name='is_in_cart',
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('items_per_page', models.PositiveIntegerField(default=12)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]