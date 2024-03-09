from django.db import models
from mainpage.models import Product
import uuid
from mainpage.models import CustomUser


# The function of generating the code for the order
def generate_order_number():
    while True:
        order_number = str(uuid.uuid4().int & (1 << 64) - 1)
        if not Order.objects.filter(order_number=order_number).exists():
            return order_number


# The product model
class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=100, unique=True, default=generate_order_number)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return self.order_number


# A new model to associate products with quantities in the order
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} ({self.quantity}x)"