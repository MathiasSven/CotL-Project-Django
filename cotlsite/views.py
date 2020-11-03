from django.shortcuts import render, redirect
from discordlogin.models import User


def index(request):
    return render(request, "cotlsite/index.html")
