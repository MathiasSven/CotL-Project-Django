from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("tools/drop-calculator", views.drop_calculator, name="drop-calculator"),
    path("activity/", views.activity, name="activity"),
    # path("report/<int:nationid>", views.report, name="report"),

    path("select2/alliance-members", views.AllianceMemberAutocomplete.as_view(), name="alliance-members-autocomplete"),
]
