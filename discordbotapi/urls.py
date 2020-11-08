from django.urls import path

from . import views

urlpatterns = [
    path("member-join", views.member_join, name="member_join"),
    path("member-remove", views.member_remove, name="member_remove"),
    path("member-update", views.member_update, name="member_update"),
    path("user-update", views.user_update, name="user_update"),
    path("members-bulk", views.members_bulk, name="members_bulk"),
]