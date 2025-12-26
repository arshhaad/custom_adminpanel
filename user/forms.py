from django import forms
from django.contrib.auth.models import User


class CustomUser(forms.ModelForm):
    username = forms.CharField(
        label="username", widget=forms.TextInput(attrs={"placeholder": "username"})
    )

    password1 = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}),
    )
    email = forms.EmailField(
        required=True, widget=forms.EmailInput(attrs={"placeholder": "Email"})
    )

    def clean(self):
        cleaned = super().clean()
        pwd = cleaned.get("password1")
        cpwd = cleaned.get("password2")
        if pwd and cpwd:
            if pwd != cpwd:
                raise forms.ValidationError("Passwords don't match.")
            if pwd and len(pwd) < 6:
                raise forms.ValidationError("Password must be at least 6 characters.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ["username", "email"]

    # def clean(self):
    #     cleaned = super().clean()
    #     pwd = cleaned.get('password')
    #     cpwd = cleaned.get('confirm_password')
    #     if pwd or cpwd:
    #         if pwd != cpwd:
    #             raise forms.ValidationError("Passwords don't match.")
    #         if pwd and len(pwd) < 6:
    #             raise forms.ValidationError("Password must be at least 6 characters.")
    #     return cleaned
