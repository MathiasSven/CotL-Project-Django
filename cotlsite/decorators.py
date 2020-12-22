from django.http import HttpResponse

from .models import Member


def allowed_users(allowed_roles=None):
    if allowed_roles is None:
        allowed_roles = []

    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            try:
                member_object = Member.objects.get(pk=request.user.pk)
            except Member.DoesNotExist:
                return HttpResponse('You must be a member of CotL to use this tool')
            else:
                if member_object.roles.filter(name__in=allowed_roles).exists() or request.user.is_superuser:
                    return view_func(request, *args, **kwargs)
                else:
                    return HttpResponse('You must be a member of CotL to use this tool')
        return wrapper_func

    return decorator
