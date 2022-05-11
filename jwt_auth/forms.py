from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label='Your name', min_length=3, max_length=13)
    email = forms.EmailField()
    password1 = forms.CharField(label='Password ', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password ', widget=forms.PasswordInput)

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data.get('username'),
            email=self.cleaned_data.get('email'),
            password=self.cleaned_data.get('password1'),
        )
        user.save()

        return user
