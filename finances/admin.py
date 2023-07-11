from constance import config
from simple_history.admin import SimpleHistoryAdmin

from django.contrib import admin

from role_permissions.models import UserRole
from .models import (
    Card,
    Payroll,
    Account,
    Bank,
    )


class CardHistoryAdmin(SimpleHistoryAdmin):
    list_display = ['number', 'bank', 'valid_until', 'is_active', 'active_since', 'current_turnover', 'operator', ]
    history_list_display = ['status']
    search_fields = ['number', ]


class PayrollHistoryAdmin(SimpleHistoryAdmin):
    history_list_display = ['status']
    search_fields = ['amount', 'card_number', 'uid', ]
    ordering = ('-updated_at', )

    def get_changeform_initial_data(self, request):
        return {'comission': config.COMISSION}

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or (request.user.role == UserRole.objects.get(name='Администратор')):
            return qs
        return qs.filter(
            operator=request.user,
            status=Payroll.Statuses.PROCESSING.value
            )

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ('status', 'operator', )
        return ()

    def get_readonly_fields(self, request, obj):
        if request.user.is_superuser:
            return (
                'created_at',
                )
        if request.user.role == UserRole.objects.get(name='Оператор'):
            return (
                'uid',
                'partner',
                'operator',
                'payment_type',
                'amount',
                'bank',
                'card_number',
                'account_number',
                'comission',
                'comission_amount',
                'created_at',
                )
        if request.user.role == UserRole.objects.get(name='Администратор'):
            return (
                'uid',
                'partner',
                'payment_type',
                'amount',
                'comission',
                'comission_amount',
                'created_at',
                )

    def get_fields(self, request, obj):
        if request.user.is_superuser:
            return (
                'partner',
                'operator',
                'payment_type',
                'amount',
                # 'remittance_amount',
                'bank',
                'card_number',
                'account_number',
                'comission',
                'comission_amount',
                'status',
                'cheque',
                'file_cheque',
                'back_url',
                'created_at',
                )
        if request.user.role == UserRole.objects.get(name='Оператор'):
            return (
                'operator',
                'payment_type',
                'amount',
                'bank',
                'card_number',
                'status',
                'cheque',
                'file_cheque',
                'created_at',
                )
        if request.user.role == UserRole.objects.get(name='Администратор'):
            return (
                'partner',
                'operator',
                'payment_type',
                'amount',
                # 'remittance_amount',
                'bank',
                'card_number',
                'comission',
                'comission_amount',
                'status',
                'cheque',
                'file_cheque',
                'back_url',
                'created_at',
                )

    def get_list_display(self, request):
        if request.user.is_superuser:
            return (
                'uid',
                'partner',
                'operator',
                'payment_type',
                'amount',
                'remittance_amount',
                'bank',
                'card_number',
                'account_number',
                'comission',
                'comission_amount',
                'status',
                'created_at',
                )
        if request.user.role == UserRole.objects.get(name='Оператор'):
            return (
                'uid',
                'payment_type',
                'amount',
                'bank',
                'card_number',
                'account_number',
                'status',
                'created_at',
                )
        if request.user.role == UserRole.objects.get(name='Администратор'):
            return (
                'uid',
                'partner',
                'operator',
                'payment_type',
                'amount',
                'remittance_amount',
                'bank',
                'card_number',
                'account_number',
                'comission',
                'comission_amount',
                'status',
                'created_at',
                )


class AccountHistoryAdmin(SimpleHistoryAdmin):
    list_display = ['user', 'balance']
    history_list_display = ['status']
    search_fields = ['partner', ]


class BankHistoryAdmin(SimpleHistoryAdmin):
    list_display = ['name', 'slug']
    history_list_display = ['status']
    search_fields = ['name', ]
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Card, CardHistoryAdmin)
admin.site.register(Payroll, PayrollHistoryAdmin)
admin.site.register(Account, AccountHistoryAdmin)
admin.site.register(Bank, BankHistoryAdmin)
