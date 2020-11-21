from django.contrib.auth.backends import BaseBackend
from .models import User


class DiscordAuthenticationBackend(BaseBackend):
    def authenticate(self, request, user):
        find_user = User.objects.filter(id=user['id'])
        if len(find_user) == 0:
            new_user = User.objects.create_user(user)
            return new_user

        find_user.update(
            discord_tag=f"{user['username']}#{user['discriminator']}",
            avatar=user['avatar'],
            public_flags=user['public_flags'],
            flags=user['flags'],
            locale=user['locale'],
            mfa_enabled=user['mfa_enabled'],
        )

        return list(find_user).pop()

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None