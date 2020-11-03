from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, user, **extra_fields):
        new_user = self.create(
            id=user['id'],
            discord_tag=f"{user['username']}#{user['discriminator']}",
            avatar=user['avatar'],
            public_flags=user['public_flags'],
            flags=user['flags'],
            locale=user['locale'],
            mfa_enabled=user['mfa_enabled'],
        )
        return new_user

    def create_user(self, user, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(user, **extra_fields)

    def create_superuser(self, user, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(user, **extra_fields)