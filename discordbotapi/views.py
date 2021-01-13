import json
from datetime import datetime, timezone

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import APIKey
from cotlsite.models import Member, Role, MemberNation

from pnwdata.models import *


# noinspection DuplicatedCode
@csrf_exempt
def member_join(request):
    if request.method == 'POST':
        if APIKey.check_key(request.headers['X-Api-Key']):
            member = json.loads(request.body)

            tmp_member, new = Member.objects.get_or_create(id=member['id'])
            tmp_member.name = member['name']
            tmp_member.discriminator = member['discriminator']
            tmp_member.avatar = member['avatar']
            tmp_member.nick = member['nick']

            tmp_member.save()
            for role in member['roles']:
                tmp_role = Role.objects.get(role_id=role['id'])
                tmp_member.roles.add(tmp_role)
            return JsonResponse({
                "POST": "Member creation successful"
            }, status=201)
        else:
            return JsonResponse({
                "error": "Wrong or no API Key provided"
            }, status=403)
    else:
        return JsonResponse({
            "error": "POST request required."
        }, status=405)


@csrf_exempt
def member_remove(request):
    if request.method == 'PUT':
        if APIKey.check_key(request.headers['X-Api-Key']):
            member = json.loads(request.body)
            try:
                Member.objects.get(id=member['id']).delete()
            except Member.DoesNotExist:
                return JsonResponse({
                    "error": "Tried to remove a member that didn't exist"
                }, status=404)
            return JsonResponse({
                "PUT": "Member deletion successful"
            }, status=200)
        else:
            return JsonResponse({
                "error": "Wrong or no API Key provided"
            }, status=403)
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=405)


@csrf_exempt
def member_update(request):
    if request.method == 'PUT':
        if APIKey.check_key(request.headers['X-Api-Key']):
            member = json.loads(request.body)
            try:
                tmp_member = Member.objects.get(id=member['id'])
            except Member.DoesNotExist:
                return JsonResponse({
                    "error": "Tried to update a member that didn't exist"
                }, status=404)
            tmp_member.nick = member['nick']
            tmp_member.save()
            try:
                roles = member['roles']
                tmp_member.roles.clear()
                for role in roles:
                    tmp_role, _ = Role.objects.get_or_create(role_id=role['id'])
                    tmp_role.name = role['name']
                    tmp_role.position = role['position']
                    tmp_role.colour = f"#{hex(role['colour']).lstrip('0x')}"
                    tmp_role.save()
                    tmp_member.roles.add(tmp_role)
            except KeyError:
                pass

            return JsonResponse({
                "PUT": "Member update successful"
            }, status=200)
        else:
            return JsonResponse({
                "error": "Wrong or no API Key provided"
            }, status=403)
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=405)


@csrf_exempt
def user_update(request):
    if request.method == 'PUT':
        if APIKey.check_key(request.headers['X-Api-Key']):
            member = json.loads(request.body)
            try:
                tmp_member = Member.objects.get(id=member['id'])
            except Member.DoesNotExist:
                return JsonResponse({
                    "error": "Tried to update a member that didn't exist"
                }, status=404)
            tmp_member.name = member['name']
            tmp_member.discriminator = member['discriminator']
            tmp_member.avatar = member['avatar']
            tmp_member.save()
            return JsonResponse({
                "PUT": "User update successful"
            }, status=200)
        else:
            return JsonResponse({
                "error": "Wrong or no API Key provided"
            }, status=403)
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=405)


@csrf_exempt
def role_create(request):
    if request.method == 'POST':
        if APIKey.check_key(request.headers['X-Api-Key']):
            role = json.loads(request.body)
            Role.objects.create(
                role_id=role['id'],
                name=role['name'],
                position=role['position'],
                colour=f"#{hex(role['colour']).lstrip('0x')}"
            )
            return JsonResponse({
                "POST": "Member creation successful"
            }, status=201)
        else:
            return JsonResponse({
                "error": "Wrong or no API Key provided"
            }, status=403)
    else:
        return JsonResponse({
            "error": "POST request required."
        }, status=405)


@csrf_exempt
def role_remove(request):
    if request.method == 'PUT':
        if APIKey.check_key(request.headers['X-Api-Key']):
            role = json.loads(request.body)
            try:
                Role.objects.get(role_id=role['id']).delete()
            except Role.DoesNotExist:
                return JsonResponse({
                    "error": "Tried to remove a role that didn't exist"
                }, status=404)
            return JsonResponse({
                "PUT": "Role removal successful"
            }, status=200)
        else:
            return JsonResponse({
                "error": "Wrong or no API Key provided"
            }, status=403)
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=405)


@csrf_exempt
def role_update(request):
    if request.method == 'PUT':
        if APIKey.check_key(request.headers['X-Api-Key']):
            role = json.loads(request.body)
            try:
                tmp_role = Role.objects.get(role_id=role['id'])
                tmp_role.name = role['name']
                tmp_role.position = role['position']
                tmp_role.colour = f"#{hex(role['colour']).lstrip('0x')}"
                tmp_role.save()
            except Role.DoesNotExist:
                Role.objects.create(role_id=role['id'], name=role['name'], position=role['position'], colour=f"#{hex(role['colour']).lstrip('0x')}")
            return JsonResponse({
                "PUT": "Successful"
            }, status=200)
        else:
            return JsonResponse({
                "error": "Wrong or no API Key provided"
            }, status=403)
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=405)


# noinspection DuplicatedCode
@csrf_exempt
def members_bulk(request):
    if request.method == 'POST':
        if APIKey.check_key(request.headers['X-Api-Key']):
            data = json.loads(request.body)
            Role.objects.all().delete()
            for member in data:
                tmp_member, new = Member.objects.get_or_create(id=member['id'])
                tmp_member.name = member['name']
                tmp_member.discriminator = member['discriminator']
                tmp_member.avatar = member['avatar']
                tmp_member.nick = member['nick']
                tmp_member.save()
                for role in member['roles']:
                    tmp_role, _ = Role.objects.get_or_create(
                        role_id=role['id'],
                        name=role['name'],
                        position=role['position'],
                        colour=f"#{hex(role['colour']).lstrip('0x')}"
                    )
                    tmp_member.roles.add(tmp_role)

            return JsonResponse({
                "POST": "Successful"
            }, status=201)
        else:
            return JsonResponse({
                "error": "Wrong or no API Key provided"
            }, status=403)
    else:
        return JsonResponse({
            "error": "POST request required."
        }, status=405)


@csrf_exempt
def link_nation(request):
    if request.method == 'POST':
        if APIKey.check_key(request.headers['X-Api-Key']):
            data = json.loads(request.body)
            try:
                member_to_link = Member.objects.get(id=data['id'])
            except Member.DoesNotExist:
                return JsonResponse({
                    "error": "Member is not on the database"
                }, status=500)
            linking_nation, _ = MemberNation.objects.get_or_create(nation_id=data['nation_id'])
            linking_nation.discord_member = member_to_link
            linking_nation.save()
            return JsonResponse({
                "POST": "Successful"
            }, status=201)
        else:
            return JsonResponse({
                "error": "Wrong or no API Key provided"
            }, status=403)
    else:
        return JsonResponse({
            "error": "POST request required."
        }, status=405)


@csrf_exempt
def bank_deposit(request):
    if request.method == 'POST':
        if APIKey.check_key(request.headers['X-Api-Key']):
            data = json.loads(request.body)
            nation, _ = Nation.objects.get_or_create(nationid=data['sender_id'])
            data['nation'] = nation
            data['deposited_on'] = datetime.strptime(data.pop('tx_datetime'), '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
            deposit_object, new = Deposit.objects.update_or_create(
                tx_id=data['tx_id'], defaults=filter_kwargs(Deposit, data)
            )
            if not new:
                return JsonResponse({
                    "error": "Tx_id already registered."
                }, status=409)
            else:
                return JsonResponse({
                    "POST": "Successful"
                }, status=201)


@csrf_exempt
def bank_withdraw(request):
    if request.method == 'POST':
        if APIKey.check_key(request.headers['X-Api-Key']):
            data = json.loads(request.body)
            nationid = data.pop('nationid')
            nation, _ = Nation.objects.get_or_create(nationid=nationid)

            holding_exists = Holdings.objects.filter(nation=nation)
            if holding_exists:
                available_holdings = holding_exists[0].available_holdings()
                for resource in data:
                    if available_holdings[resource] - int(data[resource]) < 0:
                        return JsonResponse({
                            "error": "Cannot withdraw more then available."
                        }, status=403)
                request_object = Request(nation=nation, request_type='WITHDRAW', **data)
                request_object.save()
                return JsonResponse({
                    "POST": "Successful"
                }, status=201)
            else:
                return JsonResponse({
                    "error": "Holdings does not exist."
                }, status=404)


@csrf_exempt
def bank_holdings(request):
    if request.method == 'GET':
        if APIKey.check_key(request.headers['X-Api-Key']):
            data = json.loads(request.body)
            nation, _ = Nation.objects.get_or_create(nationid=data['nationid'])

            holding_exists = Holdings.objects.filter(nation=nation)
            if holding_exists:
                holding_dict = holding_exists[0].__dict__
                holding_dict.pop('_state')
                return JsonResponse(holding_dict, status=200)
            else:
                return JsonResponse({
                    "error": "Holdings does not exist."
                }, status=404)


@csrf_exempt
def bank_loan(request):
    if request.method == 'POST':
        if APIKey.check_key(request.headers['X-Api-Key']):
            pass


@csrf_exempt
def bank_ava_holdings(request):
    if request.method == 'GET':
        if APIKey.check_key(request.headers['X-Api-Key']):
            data = json.loads(request.body)
            nation, _ = Nation.objects.get_or_create(nationid=data['nationid'])

            holding_exists = Holdings.objects.filter(nation=nation)
            if holding_exists:
                tmp_dict = holding_exists[0].available_holdings()
                tmp_dict['nation_id'] = nation.nationid
                return JsonResponse(tmp_dict, status=200)
            else:
                return JsonResponse({
                    "error": "Holdings does not exist."
                }, status=404)