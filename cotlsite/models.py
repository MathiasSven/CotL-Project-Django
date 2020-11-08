from django.db import models
from django.conf import settings

from colorfield.fields import ColorField

UserModel = settings.AUTH_USER_MODEL


class Member(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=32)
    discriminator = models.CharField(max_length=4)
    avatar = models.CharField(max_length=100)
    nick = models.CharField(max_length=32, null=True)

    user_model = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True)
    roles = models.ManyToManyField('Role')

    def display_name(self):
        if self.nick is None:
            return self.name
        else:
            return self.nick

    def __str__(self):
        return f"{self.name}#{self.discriminator}"


class Role(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=32)
    position = models.IntegerField(null=True)
    colour = ColorField()

    class Meta:
        ordering = ['-position']

    def __str__(self):
        return '%s (%s)' % (self.name, self.id)