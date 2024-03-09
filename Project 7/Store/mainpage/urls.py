from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # Main
    path('', views.store_page, name='store-page'),
    path('product/<slug:product_slug>/', views.product_detail, name='product-detail'),


    # Auth
    path('signup/', views.signup_page, name='signup-page'),
    path('login/', views.login_page, name='login-page'),
    path('log-out/', views.logout_page, name='log-out'),

    # Password
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='mainpage/password-reset.html'), name='password-reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='mainpage/password-reset-done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='mainpage/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='mainpage/password_reset_complete.html'), name='password_reset_complete'),

    # Manager work
    path('update-product/<int:product_id>/', views.update_product, name='update-product'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete-product'),
    path('create-product', views.create_product, name='create-product'),
]

