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


@admin.register(TaxRecord)
class TaxRecordAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'date', 'note', 'tax_id')

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

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'request_on', 'status')
    list_filter = ('status',)
    # exclude = ('pcname',)

    @staticmethod
    def request_link(obj):
        from django.utils.safestring import mark_safe
        return mark_safe('<a target="_blank" href="%s">%s</a>' % (obj.request_link(), "Click Here"))

    resource_fields = [f.name for f in Resources._meta.get_fields()]
    for i in ['request_on', 'nation', 'request_type', 'request_link']:
        resource_fields.append(i)
    readonly_fields = resource_fields

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False