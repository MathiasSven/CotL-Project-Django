import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import APIKey
from cotlsite.models import Member, Role


@csrf_exempt
def member_join(request):
    print(request.method)
    if request.method == 'POST':
        if APIKey.check_key(request.headers['X-Api-Key']):
            # Do stuff with member data
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
    print(request.method)
    if request.method == 'DELETE':
        if APIKey.check_key(request.headers['X-Api-Key']):
            # Do stuff with member data
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
    print(request.method)
    if request.method == 'PUT':
        if APIKey.check_key(request.headers['X-Api-Key']):
            # Do stuff with member data
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
    print(request.method)
    if request.method == 'PUT':
        if APIKey.check_key(request.headers['X-Api-Key']):
            # Do stuff with member data
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
