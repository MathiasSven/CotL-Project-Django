import configparser
import requests
from pathlib import Path
from datetime import datetime

from django.contrib.auth.models import Group
from django.db import models

from colorfield.fields import ColorField
from django.db.models.signals import post_save, m2m_changed

from discordlogin.models import User as UserModel

BASE_DIR = Path(__file__).resolve().parent.parent
config = configparser.ConfigParser()
config.read(f"{BASE_DIR}/config.ini")


# noinspection PyProtectedMember
def filter_kwargs(model, arg_dict):
    model_fields = [f.name for f in model._meta.get_fields()]
    return {k: v for k, v in arg_dict.items() if k in model_fields}


class Member(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=32, null=True)
    discriminator = models.CharField(max_length=4, null=True)
    avatar = models.CharField(max_length=100, blank=True, null=True)
    nick = models.CharField(max_length=32, blank=True, null=True)
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
            else:
                instance.groups.set(member_on_login.roles.all())

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

    @staticmethod
    def change_roles(instance, action, **kwargs):
        if action == "post_add":
            try:
                find_user = UserModel.objects.get(id=instance.id)
            except UserModel.DoesNotExist:
                return
            find_user.groups.set(instance.roles.all())

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
m2m_changed.connect(Member.change_roles, sender=Member.roles.through)


class Role(Group):
    role_id = models.BigIntegerField(primary_key=True)
    position = models.IntegerField(null=True)
    colour = ColorField()

    class Meta:
        ordering = ['-position']

    def __str__(self):
        return '%s (%s)' % (self.name, self.role_id)


class MemberNation(models.Model):
    nation_id = models.IntegerField(primary_key=True)
    nation_name = models.CharField(max_length=32, null=True)
    leader_name = models.CharField(max_length=32, null=True)
    flag_url = models.URLField(null=True)
    date_founded = models.DateTimeField(null=True)

    discord_member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)

    @classmethod
    def post_create(cls, sender, instance, created, *args, **kwargs):
        if created:
            fetched_data = requests.get(f"http://politicsandwar.com/api/nation/id={instance.nation_id}&key={config.get('pnw', 'API_KEY')}")
            fetched_data = fetched_data.json()

            if not fetched_data['success']:
                return

            instance.nation_name = fetched_data['name']
            instance.leader_name = fetched_data['leadername']
            instance.flag_url = fetched_data['flagurl']
            instance.date_founded = datetime.strptime(f"{fetched_data['founded']} +0000", '%Y-%m-%d %H:%M:%S %z')
            instance.save()

    class Meta:
        verbose_name = 'Member Nation'
        verbose_name_plural = 'Member Nations'

    def nation_link(self):
        return f"https://politicsandwar.com/nation/id={self.nation_id}"

    def days_old(self):
        timedelta = datetime.utcnow() - self.date_founded
        return timedelta.days

    def __str__(self):
        return '%s (%s)' % (self.nation_name, self.nation_id)


# PnWData Connector
post_save.connect(MemberNation.post_create, sender=MemberNation)
