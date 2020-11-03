from django.urls import path

from . import views

urlpatterns = [
    path("login", views.discord_login, name="discord_login"),
    path("logout", views.discord_logout, name="discord_logout"),
    path("user", views.get_authenticated_user, name="get_authenticated_user"),
    path("redirect", views.discord_redirect, name="discord_redirect"),
]