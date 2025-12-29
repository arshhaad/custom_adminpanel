from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class UserForm(forms.ModelForm):
    password = forms.CharField(
        required=False, widget=forms.PasswordInput, label="Password"
    )
    confirm_password = forms.CharField(
        required=False, widget=forms.PasswordInput, label="Confirm password"
    )

    class Meta:
        model = User
        fields = ["username", "email"]

    def clean(self):
        cleaned = super().clean()
        pwd = cleaned.get("password")
        cpwd = cleaned.get("confirm_password")
        if pwd or cpwd:
            if not pwd or not cpwd:
                raise forms.ValidationError(
                    "Both password fields are required to change password."
                )
            if pwd != cpwd:
                raise forms.ValidationError("Passwords don't match.")
            if len(pwd) < 8:
                raise forms.ValidationError("Password must be at least 8 characters.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        pwd = self.cleaned_data.get("password")
        if pwd:
            user.set_password(pwd)  # hash password
        if commit:
            user.save()
        return user
