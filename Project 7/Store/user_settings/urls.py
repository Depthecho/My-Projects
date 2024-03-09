from django.urls import path
from . import views

urlpatterns = [
    path('settings/', views.settings_view, name='settings'),

    path('settings/appearance/', views.appearance_settings_view, name='appearance-settings'),

    path('settings/confidentiality/', views.confidentiality_settings_view, name='confidentiality-settings'),
]
