from django import forms
from django.contrib.auth.models import User
from accounts.models import User

class UserRegistrationForm(forms.Form):
    username = forms.CharField(
        label='Username', 
        max_length=100, 
        min_length=3,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    userid = forms.DecimalField(
        label='UserId',
        max_digits=7,
        decimal_places=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    name = forms.CharField(
        label='Full name', 
        max_length=100, 
        min_length=5,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='Email', 
        max_length=20, 
        min_length=5,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Password', 
        max_length=50, 
        min_length=5,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    usertype = forms.ChoiceField(
        choices=User.USER_TYPE_CHOICES
    )
    
