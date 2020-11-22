from django.contrib import admin

from .models import Member, Role, PnWData

admin.site.register(Member)
admin.site.register(Role)
admin.site.register(PnWData)