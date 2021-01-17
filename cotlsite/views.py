import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from cotlsite.decorators import allowed_users
from cotlsite.models import filter_kwargs

from discordlogin.models import GeoData


@csrf_exempt
def home(request):
    if request.method == 'GET':
        return render(request, "cotlsite/home.html")
    elif request.method == 'POST':
        data = json.loads(request.body)
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({
                "error": "not_authenticated"
            }, status=403)
        data['data']['local_timezone_offset'] = data['minutes_offset']
        GeoData.objects.update_or_create(id=user, defaults=filter_kwargs(GeoData ,data['data']))
        return JsonResponse({
            "POST": "Successful"
        }, status=201)


def events_views(request):
    pass


def members_view(request):
    pass


@login_required
def tools_view(request):
    pass


@login_required(redirect_field_name='state')
@allowed_users(allowed_roles=['P&W Member'])
def drop_calculator(request):
    if request.method == 'POST':
        enemy_nation_id = request.POST['enemy_nation_id']

    context = {'enemy_nation_id': None}

    return render(request, "cotlsite/tools.html", context)
