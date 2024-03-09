from django.db import models
from mainpage.models import Product, CustomUser


# # Creating a model for a product in the shopping cart
class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart_quantity = models.PositiveIntegerField(default=1)