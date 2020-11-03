import os
import requests

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout

DISCORD_LOGIN_URI = os.getenv('DISCORD_LOGIN_URI')
DISCORD_CLIENT_ID = os.getenv('DISCORD_CLIENT_ID')
DISCORD_CLIENT_SECRET = os.getenv('DISCORD_CLIENT_SECRET')
DISCORD_REDIRECT_URI = os.getenv('DISCORD_REDIRECT_URI')
SCOPE = os.getenv('SCOPE')


def discord_login(request):
    return redirect(DISCORD_LOGIN_URI)


def discord_logout(request):
    logout(request)


@login_required(login_url="/oauth2/login")
def get_authenticated_user(request):
    return JsonResponse({"msg": "Authenticated"})


def discord_redirect(request):
    code = request.GET.get('code')
    user = exchange_code(code)
    discord_user = authenticate(user=user)
    discord_user = list(discord_user).pop()
    login(request, discord_user)
    return JsonResponse({"user": user})


def exchange_code(code):
    data = {
        "client_id": DISCORD_CLIENT_ID,
        "client_secret": DISCORD_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": DISCORD_REDIRECT_URI,
        "scope": SCOPE,
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post("https://discord.com/api/oauth2/token", data=data, headers=headers)
    credentials = response.json()
    access_token = credentials['access_token']
    response = requests.get("https://discord.com/api/v6/users/@me", headers={
        "Authorization": f"Bearer {access_token}"
    })
    return response.json()
