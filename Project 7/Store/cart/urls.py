from django.urls import path, include
from . import views


urlpatterns = [
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.cart_page, name='cart'),
    path('update-cart/<int:product_id>/', views.update_cart, name='update-cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove-from-cart'),
]