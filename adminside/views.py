from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.cache import never_cache

# from accounts.forms import AdminUserForm
# from django.db import IntegrityError, transaction
from .forms import UserForm
from django.db.models import Q


User = get_user_model()


@never_cache
def admin_login(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect("dashboard")
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_superuser:
                login(request, user)
                return redirect("dashboard")
            else:
                messages.error(
                    request,
                    "You are not authorized to access the admin dashboard.",
                )
                return render(request, "adminside/admin_login.html", {"form": form})
        else:
            messages.error(
                request,
                "Invalid username or password",
            )
            return render(request, "adminside/admin_login.html", {"form": form})
    else:
        form = AuthenticationForm()
    return render(request, "adminside/admin_login.html", {"form": form})


@never_cache
@login_required(login_url="admin_login")
def dashboard(request):
    if not request.user.is_superuser:
        return redirect("home")
    user_count = User.objects.count()
    recent_users = User.objects.order_by("-date_joined")[:3]
    context = {"user_count": user_count, "recent_users": recent_users}
    return render(request, "adminside/dashboard.html", context)


@never_cache
@login_required(login_url="admin_login")
def user_list(request):
    if not request.user.is_superuser:
        return redirect("home")
    users = User.objects.all()
    query = request.GET.get("q")

    if query:
        users = users.filter(Q(username__icontains=query) | Q(email__icontains=query))
    return render(request, "adminside/user_list.html", {"users": users})


@never_cache
@login_required(login_url="admin_login")
def user_add(request):
    if not request.user.is_superuser:
        return redirect("home")
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            messages.success(request, "User created.")
            return redirect("user_list")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = UserForm()

    return render(request, "adminside/user_add.html", {"form": form})


@never_cache
@login_required(login_url="admin_login")
def user_edit(request, user_id):
    if not request.user.is_superuser:
        return redirect("home")
    user = get_object_or_404(User, pk=user_id)

    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            # commit=False to handle password properly
            user_obj = form.save(commit=False)

            pwd = form.cleaned_data.get("password")
            if pwd:
                user_obj.set_password(pwd)

            user_obj.save()
            messages.success(request, "User updated successfully ✅")
            return redirect("user_list")
        else:
            messages.error(request, "Please fix the errors below ✋")
    else:
        form = UserForm(instance=user)

    return render(request, "adminside/user_edit.html", {"form": form, "user": user})


@never_cache
@login_required(login_url="admin_login")
def user_delete(request, pk):
    if not request.user.is_superuser:
        return redirect("home")
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        user.delete()
        messages.success(request, "User deleted")
        return redirect("user_list")
    return render(request, "adminside/user_delete.html", {"user": user})


@login_required(login_url="admin_login")
@never_cache
def admin_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect("admin_login")
