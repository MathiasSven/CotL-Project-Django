from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ['discord_tag']
    readonly_fields = ['id', 'discord_tag', 'avatar', 'public_flags', 'flags',
                       'locale', 'mfa_enabled', 'last_login', 'date_joined', 'groups']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False