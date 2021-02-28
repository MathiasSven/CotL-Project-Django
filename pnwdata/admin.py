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


@admin.register(Market)
class MarketAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
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


# @admin.register(TaxRecord)
# class TaxRecordAdmin(admin.ModelAdmin):
#     list_display = ('__str__', 'date', 'note', 'tax_id')
#
#     def has_add_permission(self, request):
#         return False
#
#     def has_change_permission(self, request, obj=None):
#         return False
#
#     def has_delete_permission(self, request, obj=None):
#         return False


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Aid)
class AidAdmin(admin.ModelAdmin):
    autocomplete_fields = ['nation']
    list_display = ('__str__', 'sent_on')

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


@admin.register(Holdings)
class HoldingsAdmin(admin.ModelAdmin):
    autocomplete_fields = ['nation']
    list_display = ('__str__', 'money',)

    def get_readonly_fields(self, request, obj=None):
        if obj:  # This is the case when obj is already created i.e. it's an edit
            return ['nation', 'last_updated']
        else:
            return ['last_updated']


@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    autocomplete_fields = ['nation']
    list_display = ('__str__', 'money',)

    readonly_fields = ['tx_id', 'deposited_on']

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Withdraw)
class WithdrawAdmin(admin.ModelAdmin):
    autocomplete_fields = ['nation']
    list_display = ('__str__', 'money',)
    readonly_fields = ['tx_id']

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'request_on', 'status')
    list_filter = ('status',)

    @staticmethod
    def request_link(obj):
        from django.utils.safestring import mark_safe
        return mark_safe('<a target="_blank" href="%s">%s</a>' % (obj.request_link(), "Click Here"))

    def get_readonly_fields(self, request, obj=None):
        resource_fields = [f.name for f in Resources._meta.get_fields()]
        readonly_fields = resource_fields
        if obj.request_type == 'AID':
            for i in ['request_on', 'reason', 'nation', 'request_type', 'identifier']:
                resource_fields.append(i)
            readonly_fields = resource_fields
        elif obj.request_type == 'WITHDRAW':
            for i in ['request_on', 'nation', 'request_type', 'request_link', 'identifier']:
                resource_fields.append(i)
            readonly_fields = resource_fields
        elif obj.request_type == 'LOAN':
            for i in ['request_on', 'reason', 'nation', 'request_type', 'request_link']:
                resource_fields.append(i)
            readonly_fields = resource_fields
        return readonly_fields

    def get_exclude(self, request, obj=None):
        if obj.request_type == 'AID':
            return ['pay_by', 'request_link']
        elif obj.request_type == 'WITHDRAW':
            return ['pay_by', 'reason']
        elif obj.request_type == 'LOAN':
            return ['identifier']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
