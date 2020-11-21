import os
import requests
from datetime import datetime

from django.db import models
from django.conf import settings

from colorfield.fields import ColorField
from django.db.models.signals import post_save

UserModel = settings.AUTH_USER_MODEL


class Member(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=32)
    discriminator = models.CharField(max_length=4)
    avatar = models.CharField(max_length=100)
    nick = models.CharField(max_length=32, null=True)
    roles = models.ManyToManyField('Role')

    user_model = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True)

    @classmethod
    def post_create(cls, sender, instance, created, *args, **kwargs):
        if created:
            member_on_login, new = cls.objects.get_or_create(id=instance.id)
            if new:
                member_on_login.name = instance.username
                member_on_login.discriminator = instance.discriminator
                member_on_login.avatar = instance.avatar

            member_on_login.user_model = instance
            member_on_login.save()

    def display_name(self):
        if self.nick is None:
            return self.name
        else:
            return self.nick

    def __str__(self):
        return f"{self.name}#{self.discriminator}"


# Member User Connector
post_save.connect(Member.post_create, sender=UserModel)


class Role(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=32)
    position = models.IntegerField(null=True)
    colour = ColorField()

    class Meta:
        ordering = ['-position']

    def __str__(self):
        return '%s (%s)' % (self.name, self.id)


class PnWData(models.Model):
    nation_id = models.IntegerField(primary_key=True)
    nation_name = models.CharField(max_length=32, null=True)
    leader_name = models.CharField(max_length=32, null=True)
    flag_url = models.URLField(null=True)
    date_founded = models.DateTimeField(null=True)

    discord_member = models.ForeignKey(Member, on_delete=models.CASCADE)

    @classmethod
    def post_create(cls, sender, instance, created, *args, **kwargs):
        if created:
            fetched_data = requests.get(f"http://politicsandwar.com/api/nation/id={instance.nation_id}&key={os.getenv('PNW_API_KEY')}")
            fetched_data = fetched_data.json()

            if not fetched_data['success']:
                return

            instance.nation_name = fetched_data['name']
            instance.leader_name = fetched_data['leadername']
            instance.flag_url = fetched_data['flag_url']
            instance.date_fonded = fetched_data['founded']

            instance.save()

    def nation_link(self):
        return f"https://politicsandwar.com/nation/id={self.nation_id}"

    def days_old(self):
        timedelta = datetime.utcnow() - self.date_founded
        return timedelta.days


# PnWData Connector
post_save.connect(PnWData.post_create, sender=PnWData)