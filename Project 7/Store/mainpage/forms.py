from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from .models import CustomUser, ProductComment, Product


# The user registration form
class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add 'input' class to form fields
        for fieldname in ['username', 'email', 'password1', 'password2']:
            self.fields[fieldname].widget.attrs.update({'class': 'input'})

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        # Check if password1 and password2 match
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match.")

        # Additional password validation
        password_validation.validate_password(password1, self.instance)

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        # Check if password meets your requirements
        if len(password1) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        if not any(char.isupper() for char in password1):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")
        if not any(char.islower() for char in password1):
            raise forms.ValidationError("Password must contain at least one lowercase letter.")
        if not any(char.isdigit() for char in password1):
            raise forms.ValidationError("Password must contain at least one digit.")

        # Use Django's built-in password validation
        password_validation.validate_password(password1, self.instance)

        return password1

    def clean_username(self):
        username = self.cleaned_data['username']

        # Check if the username already exists
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken. Please choose a different one.')

        return username

    def clean_email(self):
        email = self.cleaned_data['email']

        # Check if the email address already exists
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already registered. Please use a different one.')

        return email


# The user comments form
class ProductCommentForm(forms.ModelForm):
    class Meta:
        model = ProductComment
        fields = ['rating', 'comment']


# Product update form
class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'quantity', 'price', 'discount']


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'slug', 'image', 'description', 'category', 'quantity', 'price', 'discount']