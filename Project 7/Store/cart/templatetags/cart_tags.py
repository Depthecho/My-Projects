from django import template
from cart.models import CartItem


register = template.Library()


@register.filter
def cart_total_items(user):
    return CartItem.objects.filter(user=user).count()


@register.filter
def total_price(cart_items):
    total = 0
    for cart_item in cart_items:
        # Check if the product has a discount
        if cart_item.product.discount:
            discounted_price = cart_item.product.price * (1 - cart_item.product.discount / 100)
            total += discounted_price * cart_item.cart_quantity
        else:
            total += cart_item.product.price * cart_item.cart_quantity
    return total