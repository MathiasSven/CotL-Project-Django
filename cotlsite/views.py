import json

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils.html import format_html
from django.views.decorators.csrf import csrf_exempt

from cotlsite.decorators import allowed_users
from cotlsite.models import filter_kwargs

from .models import MemberNation
import pnwdata.models as pnwmodels

from discordlogin.models import GeoData
from .forms import *


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
        GeoData.objects.update_or_create(user=user, defaults=filter_kwargs(GeoData, data['data']))
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


@login_required(redirect_field_name='state')
@allowed_users(allowed_roles=['High Government', 'Low Government'])
def activity(request):
    if request.GET:
        if "nationid" in request.GET.keys():
            alliance_member = AllianceMember.objects.get(nation__nationid=request.GET['nationid'])
            return JsonResponse({
                "GET": alliance_member.get_activity()
            }, status=200)
        else:
            return JsonResponse({
                "GET": "Bad Request"
            }, status=400)
    form = AllianceMemberForm()
    return render(request, "cotlsite/activity.html", {'form': form})


@method_decorator(login_required(redirect_field_name='state'), name='get')
@method_decorator(allowed_users(allowed_roles=['High Government', 'Low Government']), name='get')
class AllianceMemberAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = AllianceMember.objects.all()

        if self.q:
            qs = qs.filter(Q(nation__nation__istartswith=self.q) | Q(nation__nationid__istartswith=self.q))

        return qs

    def get_result_label(self, item):
        member_nation = MemberNation.objects.filter(nation_id=item.nation.nationid).first()
        if member_nation is not None:
            flag_url = member_nation.flag_url
            dimensions = [25, 15]
        else:
            flag_url = ""
            dimensions = [0, 0]
        return format_html('<img style="width: {}px; height: {}px;" src="{}"> {}', dimensions[0], dimensions[1], flag_url, item.__str__().replace(" Alliance Member", ""))


from pnwdata.tables import TaxTable, WCTable, CityTable, NationGrade


@login_required(redirect_field_name='state')
@allowed_users(allowed_roles=['High Government'])
def taxes(request, tax_id):
    table1 = TaxTable(tax_id)
    table2 = WCTable(tax_id)
    table3 = CityTable(tax_id)
    table4 = NationGrade(tax_id)

    return render(request, "cotlsite/tables.html", {
        "table1": table1,
        "table2": table2,
        "table3": table3,
        "table4": table4
    })


@login_required(redirect_field_name='state')
@allowed_users(allowed_roles=['High Government'])
def dashboard(request):
    return render(request, "cotlsite/dashboard.html")