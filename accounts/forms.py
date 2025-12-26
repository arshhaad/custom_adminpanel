# accounts/forms.py
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class AdminUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password"]

    def clean_username(self):
        username = self.cleaned_data["username"]
        # case-insensitive check
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError("That username is already taken.")
        return username
