from django import forms
from django.contrib.auth import authenticate
from .models import Account


class RegistrationForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Account

        fields = [
            'name',
            'username',
            'email',
            'phone',
            'location',
            'password',
        ]


class AccountAuthenticationForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):

        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if not authenticate(email=email, password=password):
            raise forms.ValidationError("Invalid login credentials")