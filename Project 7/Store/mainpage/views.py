from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.shortcuts import get_object_or_404,render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm, ProductCommentForm, ProductUpdateForm, ProductCreateForm
from .models import Product, Category, ProductComment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from user_profile.models import UserProfile
from django.contrib.auth.models import Group


# The registration function
def signup_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after successful registration
            UserProfile.objects.create(user=user)
            login(request, user)
            return redirect('store-page')  # Redirect to the store page after signup
    else:
        form = RegistrationForm()

    return render(request, 'mainpage/signup-page.html', {'form': form})


# the authorization function
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('store-page')  # Redirect to the desired page after successful login
        else:
            # Authentication failed, display an error message
            error_message = "Invalid username or password. Please try again."
    else:
        error_message = None
    return render(request, 'mainpage/login-page.html', {'error_message': error_message})


# The logaut function
@login_required(login_url='login-page')
def logout_page(request):
    logout(request)  # Forcing the user to log out of the account
    return redirect('login-page')


# The function of displaying the main page of the store
def store_page(request):
    products = Product.objects.all().order_by('name')
    categories = Category.objects.all()
    user = request.user

    # Working with the display of products on the page (linear or grid)
    view_mode = request.GET.get('view_mode', 'grid')

    if view_mode == 'list':
        template_name = 'mainpage/store-page-list.html'
    else:
        template_name = 'mainpage/store-page.html'

    # Working with the display of the user's avatar
    profile = None
    is_manager = False

    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            pass

        # Check if the user is part of the 'Manager' group
        is_manager = user.groups.filter(name='Manager').exists()

    # Working with the search bar
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(name__icontains=search_query)

    # Working with product filtering
    filter_price_min = request.GET.get('price_min')
    filter_price_max = request.GET.get('price_max')
    sort_by = request.GET.get('sort_by')
    category = request.GET.get('category', 'all')

    if filter_price_min:
        products = products.filter(price__gte=filter_price_min)
    if filter_price_max:
        products = products.filter(price__lte=filter_price_max)

    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'rating_high':
        products = Product.objects.annotate(avg_rating=Avg('productcomment__rating')).order_by('-avg_rating', 'price')
    elif sort_by == 'rating_low':
        products = Product.objects.annotate(avg_rating=Avg('productcomment__rating')).order_by('avg_rating', 'price')

    if category != 'all':
        products = products.filter(category__name=category)

    # Processing of the form for selecting the number of products on the page
    if request.method == 'GET' and 'itemsPerPage' in request.GET:
        items_per_page = int(request.GET['itemsPerPage'])
        request.session['items_per_page'] = items_per_page
    else:
        # If the value is not specified in the form, use the stored value in the session
        items_per_page = request.session.get('items_per_page', 9)

    paginator = Paginator(products, items_per_page)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {'products': products,
               'categories': categories,
               'profile': profile,
               'search_query': search_query,
               'items_per_page': items_per_page,
               'view_mode': view_mode,
               'is_manager': is_manager}
    return render(request, template_name, context)


# The function of displaying each product separately
def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    profile = None
    user = request.user
    user_comment = None

    # Working with the display of the user's avatar
    if user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            pass

        # Working with product comments
        comments = ProductComment.objects.filter(product=product)

        user_comment = comments.filter(user=user).first()

        if request.method == 'POST':
            form = ProductCommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.product = product
                comment.save()
                return redirect('product-detail', product_slug=product_slug)
        else:
            form = ProductCommentForm()
    else:
        form = None
        comments = ProductComment.objects.filter(product=product)

    context = {
        'product': product,
        'profile': profile,
        'form': form,
        'user_comment': user_comment,
        'comments': comments,
    }
    return render(request, 'mainpage/product_detail.html', context)


@login_required(login_url='login-page')
def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ProductUpdateForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            # Redirect to the product detail page or any other desired page
            return redirect('store-page')
    else:
        form = ProductUpdateForm(instance=product)

    return render(request, 'mainpage/update-product.html', {'form': form})


@login_required(login_url='login-page')
def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    view_mode = request.GET.get('view_mode', 'grid')

    if view_mode == 'list':
        template_name = 'mainpage/store-page-list.html'
    else:
        template_name = 'mainpage/store-page.html'

    if request.method == 'POST':
        product.delete()
        return redirect('store-page')

    return render(request, template_name, {'product': product})


def create_product(request):
    if request.method == 'POST':
        form = ProductCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('store-page')
    else:
        form = ProductCreateForm()

    return render(request, 'mainpage/create-product.html', {'form': form})