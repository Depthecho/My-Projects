from django.urls import path
from . import views


urlpatterns = [
    path('add-to-favorite/<int:product_id>/', views.add_to_favorite, name='add-to-favorite'),
    path('remove-from-favorite-store/<int:product_id>/', views.remove_from_favorite_store, name='remove-from-favorite'),
    path('remove-from-favorite/<int:product_id>/', views.remove_from_favorite, name='remove-from-favorite-fav'),
    path('favorite-list/', views.favorite_list, name='favorite-list'),
]