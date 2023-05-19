from django import forms

from .models import Room
from django.contrib.auth.models import User

class RoomForm(forms.ModelForm):
    topic = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Room Topic'}))
    name = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Room Name'}))
    description = forms.CharField(required=False, label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Room Description'}))

    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']

class UserForm(forms.ModelForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Username'}))
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter Email'}))

    class Meta:
        model = User
        fields = ['username', 'email']