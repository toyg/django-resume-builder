from django import forms
from django.contrib.auth.models import User


class CreateAccountForm(forms.ModelForm):
    """
    A form for registering a new user account. Password validation is handled
    separately.
    """
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
