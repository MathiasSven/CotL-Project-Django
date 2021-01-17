from django.contrib import admin
from .models import User, GeoData


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ['discord_tag']

    @staticmethod
    def timezone(obj):
        time = obj.geodata.local_timezone_offset
        hours = abs(time) // 60
        minutes = abs(time) % 60
        return f"UTC{'-' if time > 0 else '+'}{hours}:{minutes:02d}"

    readonly_fields = ['id', 'discord_tag', 'avatar', 'public_flags', 'flags',
                       'locale', 'mfa_enabled', 'last_login', 'date_joined', 'groups', 'timezone']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(GeoData)
class GeoDataAdmin(admin.ModelAdmin):
    search_fields = ['user']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False