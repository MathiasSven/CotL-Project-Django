from django.contrib import admin
from .models import *


@admin.register(Alliance)
class AllianceAdmin(admin.ModelAdmin):
    search_fields = ['name']

    def has_module_permission(self, request):
        return False


@admin.register(Nation)
class NationAdmin(admin.ModelAdmin):
    search_fields = ['nation']
    autocomplete_fields = ['alliance']

    def has_module_permission(self, request):
        return False


@admin.register(AllianceMember)
class AllianceMemberAdmin(admin.ModelAdmin):
    search_fields = ['nation__nation']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    autocomplete_fields = ['nation']
    list_display = ('__str__', 'borrowing_date', 'payed')
    list_filter = ('payed',)

    readonly_fields = ['payed_on']


@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    autocomplete_fields = ['nation']
    list_display = ('__str__', 'deposited_on',)

    readonly_fields = ['deposited_on']
