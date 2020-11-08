import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import APIKey
from cotlsite.models import Member, Role


# class ApiIO(object):
#     def __init__(self, _id, name=None, discriminator=None, avatar=None, nick=None):
#         self.id = _id
#         self.name = name
#         self.discriminator = discriminator
#         self.avatar = avatar
#         self.nick = nick


@csrf_exempt
def member_join(request):
    if request.method == 'POST':
        if APIKey.check_key(request.headers['X-Api-Key']):
            member = json.loads(request.body)
            tmp_member = Member.objects.create(
                id=member['id'],
                name=member['name'],
                discriminator=member['discriminator'],
                avatar=member['avatar'],
                nick=member['nick']
            )
            for role in member['roles']:
                tmp_role = Role.objects.get(id=role['id'])
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
def member_remove(request):
    if request.method == 'DELETE':
        if APIKey.check_key(request.headers['X-Api-Key']):
            member = json.loads(request.body)
            Member.objects.get(id=member['id']).delete()
            return JsonResponse({
                "DELETE": "Successful"
            }, status=200)
        else:
            return JsonResponse({
                "error": "Wrong or no API Key provided"
            }, status=403)
    else:
        return JsonResponse({
            "error": "DELETE request required."
        }, status=405)


@csrf_exempt
def member_update(request):
    if request.method == 'PUT':
        if APIKey.check_key(request.headers['X-Api-Key']):
            member = json.loads(request.body)
            tmp_member = Member.objects.get(member['id'])
            tmp_member.roles.clear()

            tmp_member.name = member['name']
            tmp_member.discriminator = member['discriminator']
            tmp_member.avatar = member['avatar']
            tmp_member.nick = member['nick']
            tmp_member.save()
            for role in member['roles']:
                tmp_role, _ = Role.objects.get_or_create(
                    id=role['id'],
                    name=role['name'],
                    position=role['position'],
                    colour=f"#{hex(role['colour']).lstrip('0x')}"
                )
                tmp_member.roles.add(tmp_role)
            return JsonResponse({
                "POST": "Successful"
            }, status=200)
        else:
            return JsonResponse({
                "error": "Wrong or no API Key provided"
            }, status=403)
    else:
        return JsonResponse({
            "error": "PATCH request required."
        }, status=405)


@csrf_exempt
def user_update(request):
    if request.method == 'PUT':
        if APIKey.check_key(request.headers['X-Api-Key']):
            member = json.loads(request.body)
            tmp_member = Member.objects.get(member['id'])
            tmp_member.name = member['name']
            tmp_member.discriminator = member['discriminator']
            tmp_member.avatar = member['avatar']
            tmp_member.save()
            return JsonResponse({
                "POST": "Successful"
            }, status=200)
        else:
            return JsonResponse({
                "error": "Wrong or no API Key provided"
            }, status=403)
    else:
        return JsonResponse({
            "error": "PATCH request required."
        }, status=405)


@csrf_exempt
def members_bulk(request):
    if request.method == 'POST':
        if APIKey.check_key(request.headers['X-Api-Key']):
            data = json.loads(request.body)
            Member.objects.all().delete()
            Role.objects.all().delete()
            for member in data:
                tmp_member = Member.objects.create(
                    id=member['id'],
                    name=member['name'],
                    discriminator=member['discriminator'],
                    avatar=member['avatar'],
                    nick=member['nick']
                )
                for role in member['roles']:
                    tmp_role, _ = Role.objects.get_or_create(
                        id=role['id'],
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
