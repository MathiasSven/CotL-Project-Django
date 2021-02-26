from rest_framework import permissions, viewsets

from .models import AllianceMember, Trade
from .serializers import *


class RestrictedDjangoObjectPermissions(permissions.DjangoModelPermissions):
    perms_map = permissions.DjangoModelPermissions.perms_map
    perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']


class AllianceMemberView(viewsets.ReadOnlyModelViewSet):
    queryset = AllianceMember.objects.all()
    serializer_class = AllianceMemberSerializer
    permission_classes = [RestrictedDjangoObjectPermissions]


class TradesView(viewsets.ReadOnlyModelViewSet):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer
    permissions = [permissions.AllowAny]
