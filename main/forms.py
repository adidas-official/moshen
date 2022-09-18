from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Order


class RegisterForm(UserCreationForm):
    username = forms.EmailField(required=True)
    transpass1 = forms.CharField(required=True, max_length=24, min_length=8)
    transpass2 = forms.CharField(required=True, max_length=24, min_length=8)
    invitecode = forms.CharField(required=True, max_length=32, min_length=32)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'invitecode', 'transpass1', 'transpass2']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['product', 'amount']
