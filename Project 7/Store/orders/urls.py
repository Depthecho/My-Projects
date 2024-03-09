from django.urls import path
from . import views

urlpatterns = [
    path('add_to_order/', views.add_to_order, name='add_to_order'),
    path('orders/', views.orders_page, name='orders'),
    path('order/<int:order_id>/', views.order_detail, name='order-detail'),
]
