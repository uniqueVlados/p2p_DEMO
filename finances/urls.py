from django.urls import path

from .views import (
    PayrollReplenishCreateView,
    PayrollReplenishPayedView,
    PayrollWithdrawCreateView,
    PayrollWithdrawRequestView,
    BalanceRetrieveView,
    PayrollStatusRetrieveView,
    PayrollsListView,
    DaysPayrollsAmountsView,
    PayrollGetView,
    get_payroll_statuses,
    get_payment_types,
)

'''
withdraw/ - первичный запрос на списание от сервиса партнёра.
Указывается сумма, проверяется баланс партнера, создается платежное
поручение без номера карты.

withdraw-request/ - финальный запрос на списание с формы платёжного сервиса.
Указывается номер карты, он вносится в платежное поручение, у платежки
устанавливается статус В обработке, оператору поступает сигнал.
'''

urlpatterns = [
    path('replenish/', PayrollReplenishCreateView.as_view()),
    path('withdraw/', PayrollWithdrawCreateView.as_view()),
    path('withdraw-request/', PayrollWithdrawRequestView.as_view()),
    path('get-balance/', BalanceRetrieveView.as_view()),
    path('get-payment-status/', PayrollStatusRetrieveView.as_view()),
    path('get-payrolls/', PayrollsListView.as_view()),
    path('get-days-amounts/', DaysPayrollsAmountsView.as_view()),
    path('payed-request/', PayrollReplenishPayedView.as_view()),
    path('get-payroll-by-uid/', PayrollGetView.as_view()),
    path('get-payroll-statuses/', get_payroll_statuses),
    path('get-payment-types/', get_payment_types),
]
