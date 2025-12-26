from django.urls import path

# from django.views.generic import RedirectView
from . import views


urlpatterns = [
    path("login/", views.admin_login, name="admin_login"),
    path("logout/", views.admin_logout, name="admin_logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    # users...
    path("users/", views.user_list, name="user_list"),
    path("users/add/", views.user_add, name="user_add"),
    path("users/<int:user_id>/edit/", views.user_edit, name="user_edit"),
    path("users/<int:pk>/delete/", views.user_delete, name="user_delete"),
]
