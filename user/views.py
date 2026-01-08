from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from .forms import CustomUser
from django.contrib import messages



# INDEX
@never_cache
def index_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    return render(request, "index.html")


# HOME
@never_cache
def home_view(request):
    if not request.user.is_authenticated:
        return redirect("index")
    return render(request, "home.html")


# LOGOUT
@never_cache
def logout_view(request):
    if not request.user.is_authenticated:
        return redirect("login")
    logout(request)
    return redirect("index")


# LOGIN
@never_cache
def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("home")
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})


# SIGNUP
@never_cache
def signin_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = CustomUser(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Signup successful Please login to continue.")
            return redirect("login")
    else:
        form = CustomUser()
    return render(request, "signin.html", {"form": form})
