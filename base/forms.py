from django import forms

from django.contrib.auth.forms import UserCreationForm
from .models import Room, User

class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Name'}))
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Username'}))
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter Email'}))
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Enter Password'}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Re-enter Password'}))

    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']

class RoomForm(forms.ModelForm):
    topic = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Room Topic'}))
    name = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Room Name'}))

    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']

class UserForm(forms.ModelForm):
    name = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Name'}))
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Username'}))
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter Email'}))

    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']