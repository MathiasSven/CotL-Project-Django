import os
import requests
from datetime import datetime

from django.db import models

from colorfield.fields import ColorField
from django.db.models.signals import post_save

from discordlogin.models import User as UserModel


class Member(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=32, null=True)
    discriminator = models.CharField(max_length=4, null=True)
    avatar = models.CharField(max_length=100, null=True)
    nick = models.CharField(max_length=32, null=True)
    roles = models.ManyToManyField('Role')

    @classmethod
    def post_login_create(cls, sender, instance, created, *args, **kwargs):
        if created:
            try:
                member_on_login = cls.objects.get(id=instance.id)
            except cls.DoesNotExist:
                cls.objects.create(
                    id=instance.id,
                    name=instance.username(),
                    discriminator=instance.discriminator(),
                    avatar=instance.avatar
                )

    @staticmethod
    def post_member_save(sender, instance, created, *args, **kwargs):
        if not created:
            find_user = UserModel.objects.filter(id=instance.id)

            if len(find_user) == 0:
                return

            find_user.update(
                discord_tag=f"{instance.name}#{instance.discriminator}",
                avatar=instance.avatar,
            )

    def display_name(self):
        if self.nick is None:
            return self.name
        else:
            return self.nick

    def __str__(self):
        return f"{self.name}#{self.discriminator}"


# Member User Connectors
post_save.connect(Member.post_login_create, sender=UserModel)
post_save.connect(Member.post_member_save, sender=Member)


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

    discord_member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)

    @classmethod
    def post_create(cls, sender, instance, created, *args, **kwargs):
        if created:
            fetched_data = requests.get(f"http://politicsandwar.com/api/nation/id={instance.nation_id}&key={os.getenv('PNW_API_KEY')}")
            fetched_data = fetched_data.json()

            if not fetched_data['success']:
                return

            instance.nation_name = fetched_data['name']
            instance.leader_name = fetched_data['leadername']
            instance.flag_url = fetched_data['flagurl']
            instance.date_founded = datetime.strptime(f"{fetched_data['founded']} +0000", '%Y-%m-%d %H:%M:%S %z')
            instance.save()

    def nation_link(self):
        return f"https://politicsandwar.com/nation/id={self.nation_id}"

    def days_old(self):
        timedelta = datetime.utcnow() - self.date_founded
        return timedelta.days


# PnWData Connector
post_save.connect(PnWData.post_create, sender=PnWData)
