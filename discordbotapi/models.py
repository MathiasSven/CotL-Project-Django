from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password, check_password


class APIKey(models.Model):
    api_key = models.CharField(max_length=256)

    @staticmethod
    def generate_key():
        text_api_key = BaseUserManager().make_random_password(18)
        APIKey.objects.create(api_key=make_password(text_api_key))
        return text_api_key

    @staticmethod
    def check_key(api_key):
        for encoded in APIKey.objects.values('api_key'):
            if check_password(api_key, encoded['api_key']):
                return True

    class Meta:
        verbose_name = "API Key"
        verbose_name_plural = "API Keys"

    def __str__(self):
        return f"API Key ({self.pk})"