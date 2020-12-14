from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from cotlsite.decorators import allowed_users


def home(request):
    return render(request, "cotlsite/home.html")


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
    return render(request, "cotlsite/tools.html")