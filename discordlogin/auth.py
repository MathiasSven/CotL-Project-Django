from django.contrib.auth.backends import BaseBackend
from .models import User


class DiscordAuthenticationBackend(BaseBackend):
    def authenticate(self, request, user):
        find_user = User.objects.filter(id=user['id'])
        if len(find_user) == 0:
            print("User was not found. Saving...")
            new_user = User.objects.create_user(user)
            return new_user
        return find_user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None