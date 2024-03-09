from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from mainpage.models import Product, Category
from .models import CartItem
from user_profile.models import UserProfile


# The function of adding a product to the cart
@login_required(login_url='login-page')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user

    # Trying to find an existing product in the user's cart
    cart_item, created = CartItem.objects.get_or_create(user=user, product=product)

    if not created:
        # If the product was already in the cart, we increase its quantity by 1
        cart_item.cart_quantity += 1
        cart_item.save()

    return redirect('store-page')


# Cart display function
@login_required(login_url='login-page')
def cart_page(request):
    user = request.user
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = None

    cart_items = CartItem.objects.filter(user=request.user)
    total_quantity = cart_items.aggregate(total_quantity=Sum('cart_quantity'))['total_quantity']

    items_per_page = 12

    paginator = Paginator(cart_items, items_per_page)
    page = request.GET.get('page')

    try:
        cart_items = paginator.page(page)
    except PageNotAnInteger:
        cart_items = paginator.page(1)
    except EmptyPage:
        cart_items = paginator.page(paginator.num_pages)

    context = {'cart_items': cart_items, 'total_quantity': total_quantity, 'profile': profile}

    return render(request, 'cart/cart-page.html', context)


# Cart update function
@login_required(login_url='login-page')
def update_cart(request, product_id):
    if request.method == 'POST':
        # Get the new cart_quantity from the form
        new_cart_quantity = request.POST.get('cart_quantity')

        # Find the correct CartItem based on the product_id
        cart_item = CartItem.objects.filter(product_id=product_id, user=request.user).first()

        if cart_item:
            # Getting the cart_quantity of the available product in the database
            available_quantity = cart_item.product.quantity

            # Check if the new cart_quantity is valid
            if 1 <= int(new_cart_quantity) <= available_quantity:
                cart_item.cart_quantity = new_cart_quantity
                cart_item.save()
            else:
                messages.error(request, 'The requested cart_quantity exceeds the available quantity.')
        else:
            messages.error(request, 'Cart item not found for the given product.')

        return redirect('cart')


# The function of removing a product from the cart
@login_required(login_url='login-page')
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user

    # Trying to find an existing product in the user's cart
    try:
        cart_item = CartItem.objects.get(user=user, product=product)
        if cart_item.cart_quantity > 1:
            # If the user has more than one copy of the product, reduce the cart_quantity by 1
            cart_item.cart_quantity -= 1
            cart_item.save()
        else:
            # If the user has only one copy of the product, we remove it from the basket
            cart_item.delete()
    except CartItem.DoesNotExist:
        pass

    return redirect('cart')