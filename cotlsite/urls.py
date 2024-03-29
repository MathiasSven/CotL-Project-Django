from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("tools/drop-calculator", views.drop_calculator, name="drop-calculator"),
    path("activity/", views.activity, name="activity"),

    path("report/dashboard", views.dashboard, name="dashboard"),
    path("report/taxes/<int:tax_id>", views.taxes, name="taxes"),
    path("report/income/<int:turns>", views.income, name="income"),

    path("report/milcom/", views.milcom, name="milcom"),


    path("select2/alliance-members", views.AllianceMemberAutocomplete.as_view(), name="alliance-members-autocomplete"),
    path("api/discord-member/<int:user_id>", views.discord_member, name="discord-member"),

    path("api/discord-user/<int:nationid>", views.discord_user, name="discord-user"),
    path("api/linked-nation/<int:user_id>", views.linked_nation, name="linked-nation"),
]
