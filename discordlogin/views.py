import configparser
import os
import requests
from pathlib import Path

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout

BASE_DIR = Path(__file__).resolve().parent.parent
config = configparser.ConfigParser()
config.read(f"{BASE_DIR}/config.ini")

DISCORD_CLIENT_ID = config.get("discordlogin", "DISCORD_CLIENT_ID")
DISCORD_REDIRECT_URI = config.get("discordlogin", "DISCORD_REDIRECT_URI")
SCOPE = config.get("discordlogin", "SCOPE")

DISCORD_LOGIN_URI = f"https://discord.com/api/oauth2/authorize?client_id={DISCORD_CLIENT_ID}&redirect_uri={DISCORD_REDIRECT_URI}&response_type=code&scope={SCOPE}"

DISCORD_CLIENT_SECRET = os.getenv('DISCORD_CLIENT_SECRET')


def discord_login(request):
    return redirect(DISCORD_LOGIN_URI)


def discord_logout(request):
    logout(request)
    return redirect("/")


@login_required(login_url="/oauth2/login")
def get_authenticated_user(request):
    return JsonResponse({"msg": "Authenticated"})


def discord_redirect(request):
    code = request.GET.get('code')
    state = request.GET.get('state')
    user = exchange_code(code)
    discord_user = authenticate(user=user)
    discord_user = discord_user
    login(request, discord_user)
    # return JsonResponse({"user": user})
    if state:
        return redirect(state)
    return redirect("/")


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
