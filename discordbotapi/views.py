import json
from datetime import datetime, timezone

from django.core.exceptions import ValidationError
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
                tmp_role_list = []
                for role in roles:
                    tmp_role, _ = Role.objects.get_or_create(role_id=role['id'])
                    tmp_role.name = role['name']
                    tmp_role.position = role['position']
                    tmp_role.colour = f"#{hex(role['colour']).lstrip('0x')}"
                    tmp_role.save()
                    tmp_role_list.append(tmp_role)

                tmp_member.roles.clear()
                tmp_member.roles.add(*tmp_role_list)
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
                }, status=404)
            linking_nation, _ = MemberNation.objects.get_or_create(nation_id=data['nation_id'])
            unlinking_nation = member_to_link.membernation if MemberNation.objects.filter(discord_member=member_to_link).exists() else None
            linking_nation.discord_member = member_to_link
            try:
                linking_nation.validate_unique(exclude='nation_id')
            except ValidationError:
                unlinking_nation.discord_member = None
                unlinking_nation.save()
            finally:
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
def aid_request(request):
    if request.method == 'POST':
        if APIKey.check_key(request.headers['X-Api-Key']):
            data = json.loads(request.body)
            nationid = data.pop('nationid')
            nation, _ = Nation.objects.get_or_create(nationid=nationid)
            request_object = Request(nation=nation, request_type='AID', **data)
            request_object.save()
            return JsonResponse({
                "POST": "Successful"
            }, status=201)


@csrf_exempt
def aid_update(request):
    if request.method == 'PUT':
        if APIKey.check_key(request.headers['X-Api-Key']):
            data = json.loads(request.body)
            aid_request_exists = Request.objects.filter(identifier=data['identifier'], request_type='AID')
            if aid_request_exists:
                aid_request_object = aid_request_exists[0]
                aid_request_object.status = data['status']
                aid_request_object.save()
                return JsonResponse({
                    "PUT": "Successful"
                }, status=202)
            else:
                return JsonResponse({
                    "error": "Request does not exist."
                }, status=404)


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


@csrf_exempt
def bank_loan(request):
    if request.method == 'POST':
        if APIKey.check_key(request.headers['X-Api-Key']):
            data = json.loads(request.body)
            nationid = data.pop('nationid')
            data['pay_by'] = datetime.strptime(data.pop('date'), '%Y/%m/%d').replace(tzinfo=timezone.utc)
            nation, _ = Nation.objects.get_or_create(nationid=nationid)

            request_object = Request(nation=nation, request_type='LOAN', **data)
            request_object.save()
            return JsonResponse({
                "POST": "Successful"
            }, status=201)


@csrf_exempt
def active_loans(request):
    if request.method == 'GET':
        if APIKey.check_key(request.headers['X-Api-Key']):
            data = json.loads(request.body)
            nation, _ = Nation.objects.get_or_create(nationid=data['nationid'])
            loans_query = Loan.objects.filter(nation=nation, payed=False)
            if loans_query:
                return JsonResponse({
                    'data': list(loans_query.values()),
                }, status=200)
            else:
                return JsonResponse({
                    'GET': 'Not Found',
                }, status=404)


@csrf_exempt
def payback_loan(request):
    if request.method == 'POST':
        if APIKey.check_key(request.headers['X-Api-Key']):
            data = json.loads(request.body)
            loan_object = Loan.objects.get(pk=data['loan_id'])
            assert loan_object.nation.nationid == data['nationid']

            holding_exists = Holdings.objects.filter(nation__nationid=data['nationid'])
            if holding_exists:
                holdings_object = holding_exists[0]
                ava_holdings_dict = holdings_object.available_holdings()
                loan_dict = filter_kwargs(Resources, loan_object.__dict__)
                for resource in loan_dict:
                    if loan_dict[resource] > ava_holdings_dict[resource]:
                        return JsonResponse({
                            "error": "not enough resources to pay the loan"
                        }, status=404)
                    setattr(holdings_object, resource, getattr(holdings_object, resource) - loan_dict[resource])
                holdings_object.save()
                loan_object.payed = True
                loan_object.save()
                return JsonResponse({
                    "POST": "Successful"
                }, status=202)
            else:
                return JsonResponse({
                    "error": "no holdings ever registered"
                }, status=404)
