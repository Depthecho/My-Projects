from _decimal import Decimal
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


# The model of the store's product categories
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# The store's product model
class Product(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    slug = models.SlugField(max_length=200, blank=False, null=False, default="")
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default=0)

    def __str__(self):
        return self.name

    @property
    def discounted_price(self):
        if self.discount is not None and 0 < self.discount < 100:
            discount_percent = Decimal(self.discount) / Decimal(100)
            discounted_amount = self.price * discount_percent
            return self.price - discounted_amount
        return self.price


# User creation model
class CustomUserManager(BaseUserManager):
    # Function to add a user
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # Function to add a superuser
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


# The model of a regular user
class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True, db_index=True, null=False)
    email = models.EmailField(unique=True, null=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    favorite_products = models.ManyToManyField(Product, related_name='favorited_by')
    cart_products = models.ManyToManyField(Product, related_name='added_to_carts_by')

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


# The comment model
class ProductComment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(max_length=3000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'product']  # One comment per user for each product

    def __str__(self):
        return f'Comment by {self.user.username} on {self.product.name}'