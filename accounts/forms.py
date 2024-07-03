from django.contrib.auth.forms import UserCreationForm
from .models import *
from django import forms


class SignupForm(UserCreationForm):

    def __init__(self, *args, **kwargs) -> None:
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = "mb-2 px-4 py-2 rounded-lg border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-lime-300 w-full"
        self.fields['password2'].widget.attrs['class'] = "mb-2 px-4 py-2 rounded-lg border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-lime-300 w-full"
        self.fields['password1'].label = "Mot de pass"
        self.fields['password2'].label = "Confirmez votre mot de pass"

    class Meta:
        model = CustomUser
        fields = (
            'email', 'first_name',
            'last_name',
            'password1',
            'password2',
        )
        labels = {
            'email': 'Email',
            'first_name': 'Prenoms',
            'last_name': 'Nom',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-lg border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-lime-300 w-full"}),
            'email': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-lg border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-lime-300 w-full"}),
            'first_name': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-lg border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-lime-300 w-full"}),
            'last_name': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-lg border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-lime-300 w-full"}),
            'phone': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-lg border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-lime-300 w-full"}),
        }
