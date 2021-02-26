from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('alliance-members', views.AllianceMemberView)
router.register('trades', views.TradesView)

urlpatterns = [
    path('', include(router.urls)),
]
