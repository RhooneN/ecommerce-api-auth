from django import forms
from .models import Profile
from django.contrib.auth.models import User

class CustomerSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    business_name = forms.CharField(max_length=60)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'business_name', 'password']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'profile_picture']