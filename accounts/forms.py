from django.contrib.auth.forms import UserCreationForm
from .models import *
from django import forms


class SignupForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(SignupForm, self).__init__(*args, **kwargs)

        if user and user.role.sec_level < 3:
            self.fields.pop('role')

        if self.instance and self.instance.pk:
            # If the form is being used to edit an existing user, remove password fields
            self.fields.pop('password1')
            self.fields.pop('password2')
        else:
            # Apply custom attributes to password fields
            self.fields['password1'].widget.attrs['class'] = "mb-2 px-4 py-2 rounded-lg border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-lime-300 w-full"
            self.fields['password2'].widget.attrs['class'] = "mb-2 px-4 py-2 rounded-lg border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-lime-300 w-full"
            self.fields['password1'].label = "Mot de pass"
            self.fields['password2'].label = "Confirmez votre mot de pass"

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'first_name',
            'role',
            'last_name',
        )
        labels = {
            'email': 'Email',
            'first_name': 'Prenoms',
            'last_name': 'Nom',
        }
        widgets = {
            'role': forms.Select(attrs={'class': "input_selector mb-2 px-4 py-2 rounded-lg border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-lime-300 w-full"}),
            'username': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-lg border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-lime-300 w-full"}),
            'email': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-lg border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-lime-300 w-full"}),
            'first_name': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-lg border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-lime-300 w-full"}),
            'last_name': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-lg border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-lime-300 w-full"}),
            'phone': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-lg border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-lime-300 w-full"}),
        }


class EditUserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(EditUserForm, self).__init__(*args, **kwargs)

        if user and user.role.sec_level < 3:
            self.fields.pop('role')

    class Meta:
        model = CustomUser
        fields = (
            'role',
            'email',
            'first_name',
            'last_name',
            'username',
        )
        labels = {
            'email': 'Email',
            'first_name': 'Prenoms',
            'last_name': 'Nom',
            'username': "Nom d'utilisateur",
            'phone': 'Téléphone',
        }
        widgets = {
            'role': forms.Select(attrs={'class': "input_selector mb-2 px-4 py-2 rounded-lg border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-lime-300 w-full"}),
            'email': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-lg border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-lime-300 w-full"}),
            'first_name': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-lg border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-lime-300 w-full"}),
            'last_name': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-lg border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-lime-300 w-full"}),
            'username': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-lg border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-lime-300 w-full"}),
            'phone': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-lg border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-lime-300 w-full"}),
        }


class ProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProfileForm, self).__init__(*args, **kwargs)

        if user and user.role.sec_level < 3:
            self.fields.pop('store')

    class Meta:
        model = Profile
        fields = '__all__'
        exclude=('user',)
        labels = {
            'sex': 'Sexe',
            'store': 'Boutique',
            'phone': 'Téléphone',
        }
        widgets = {
            'sex': forms.Select(attrs={'class': "input_selector mb-2 px-4 py-2 rounded-lg border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-lime-300 w-full"}),
            'store': forms.Select(attrs={'class': "input_selector mb-2 px-4 py-2 rounded-lg border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-lime-300 w-full"}),
            'phone': forms.TextInput(attrs={'class': "mb-2 px-4 py-2 rounded-lg border border-gray-200 focus:border-none focus:outline-none focus:ring-1 focus:ring-lime-300 w-full"}),
        }
