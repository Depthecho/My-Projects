from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from .models import Order, OrderProduct
from mainpage.models import Product
from cart.models import CartItem
from user_profile.models import UserProfile


# The order page display function
@login_required(login_url='login-page')
def orders_page(request):
    user = request.user

    # Working with the display of the user's avatar
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = None

    all_orders = Order.objects.filter(user=user).order_by('-order_date')

    orders_per_page = 14

    paginator = Paginator(all_orders, orders_per_page)
    page = request.GET.get('page')

    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)

    context = {
        'profile': profile,
        'orders': orders,
    }

    return render(request, 'orders/orders_page.html', context)


# The function of adding products to the order
@login_required(login_url='login-page')
def add_to_order(request):
    user = request.user
    order, created = Order.objects.get_or_create(user=user, total_price=0)

    # Get all the items in the current user's cart
    cart_items = CartItem.objects.filter(user=user)

    # Create a list to keep track of unique product IDs
    product_ids = []

    for cart_item in cart_items:
        product = cart_item.product
        product.quantity -= cart_item.cart_quantity
        product.save()
        # Check if the product ID is not already in the list
        if product.id not in product_ids:
            order.products.add(product)
            product_ids.append(product.id)

            # Create an OrderProduct instance for the product in the order
            order_product, _ = OrderProduct.objects.get_or_create(order=order, product=product)

            # Update the quantity in the OrderProduct model
            order_product.quantity += cart_item.cart_quantity
            order_product.save()

        # Update the total_price after adding the product
        order.total_price += product.price * cart_item.cart_quantity  # Update the total_price using cart_quantity

    # Removing items from the shopping cart after purchasing an item
    cart_items.delete()

    order.save()

    return redirect('orders')


# The function of displaying each order separately
@login_required(login_url='login-page')
def order_detail(request, order_id):
    user = request.user

    # Working with the display of the user's avatar
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = None

    # Getting an order from a request
    order = get_object_or_404(Order, id=order_id, user=user)

    order_products = OrderProduct.objects.filter(order=order)

    context = {
        'order': order,
        'profile': profile,
        'order_products': order_products,
    }

    return render(request, 'orders/order_detail.html', context)