from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('update-profile/', views.update_profile, name='update-profile'),
    path('delete-profile/', views.delete_profile, name='delete-profile'),
]