from django.urls import path

from . import views

urlpatterns = [
    path("member-join", views.member_join, name="member_join"),
    path("member-remove", views.member_remove, name="member_remove"),
    path("member-update", views.member_update, name="member_update"),
    path("user-update", views.user_update, name="user_update"),
    path("role-create", views.role_create, name="role_create"),
    path("role-remove", views.role_remove, name="role_remove"),
    path("role-update", views.role_update, name="role_update"),
    path("members-bulk", views.members_bulk, name="members_bulk"),
    path("link-nation", views.link_nation, name="link_nation"),

    path("bank-deposit", views.bank_deposit, name="bank_deposit"),
    path("bank-withdraw", views.bank_withdraw, name="bank_withdraw"),
    path("bank-holdings", views.bank_holdings, name="bank_holdings"),
    path("bank-loan", views.bank_loan, name="bank_loan"),

    path("bank-ava-holdings", views.bank_ava_holdings, name="bank-ava-holdings"),
]