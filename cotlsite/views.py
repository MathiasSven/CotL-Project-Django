from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from discordlogin.models import User


def home(request):
    return render(request, "cotlsite/home.html")


def events_views(request):
    pass


def members_view(request):
    pass


@login_required
def tools_view(request):
    pass