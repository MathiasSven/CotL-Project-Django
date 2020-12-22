from django.contrib import admin

from .models import Member, Role, MemberNation

admin.site.register(MemberNation)
admin.site.register(Member)
admin.site.register(Role)