import math
from collections import defaultdict
from datetime import datetime, date, timedelta
from rest_framework.generics import (
    GenericAPIView,
    )
from rest_framework.response import Response

from django.db.models import Sum

# from users.services import get_user_by_secret_key

from utils import error
from ..models import (
    Payroll,
    )
from ..serializers import (
    PayrollListSerializer,
    )


# TODO добавить разрешения
class DaysPayrollsAmountsView(GenericAPIView):
    serializer_class = PayrollListSerializer

    def get(self, request):

        partner = self.request.user
        if not partner:
            return error(404, 'Партнер не найден.')

        # Количество дней для отчёта по умолчанию (если date_from не указана)
        days_ago = 7

        date_from = self.request.query_params.get('date_from')
        if date_from:
            date_from = datetime.strptime(date_from, "%d.%m.%Y").date()
        else:
            date_from = date.today() - timedelta(days=days_ago)

        date_until = self.request.query_params.get('date_until')
        if date_until:
            date_until = datetime.strptime(date_until + " 23:59:59", "%d.%m.%Y %H:%M:%S").date()
        else:
            date_until = date.today()

        page_size = int(self.request.query_params.get('page_size'))
        if not page_size:
            page_size = 10

        num_days = (date_until - date_from).days
        days = [date_until - timedelta(days=i) for i in range(num_days + 1)]
        payment_types = [
            Payroll.PaymentTypes.REPLENISHMENT,
            Payroll.PaymentTypes.WITHDRAWL,
            ]
        statuses = [
            Payroll.Statuses.APPROVED,
            Payroll.Statuses.FAILED,
        ]

        days_amounts = []

        for day in days:
            stringified_day = datetime.strftime(day, "%Y.%m.%d")
            day_results = {}
            day_results['date'] = stringified_day
            for payment_type in payment_types:
                status = Payroll.Statuses.APPROVED
                day_amount = Payroll.objects.filter(
                    partner=partner,
                    created_at__range=(
                        day - timedelta(days=1),
                        day + timedelta(days=1)
                        ),
                    payment_type=payment_type,
                    status=status,
                    ).aggregate(Sum('amount'))['amount__sum']
                if day_amount:
                    day_results[payment_type] = f'{day_amount:0.2f}'
                else:
                    day_results[payment_type] = '0.00'
            days_amounts.append(day_results)

        days_amounts_sorted = sorted(days_amounts, key=lambda x: x['date'], reverse=True)

        amounts_for_period = defaultdict(dict)
        for payment_type in payment_types:
            for status in statuses:
                period_amount = Payroll.objects.filter(
                    partner=partner,
                    created_at__range=(
                        date_from - timedelta(days=1),
                        date_until + timedelta(days=1)
                        ),
                    payment_type=payment_type,
                    status=status,
                    ).aggregate(Sum('amount'))['amount__sum']
                if period_amount:
                    amounts_for_period[payment_type][status] = f'{period_amount:0.2f}'
                else:
                    amounts_for_period[payment_type][status] = '0.00'

        num_records = len(days_amounts_sorted)
        num_pages = math.ceil(num_records / page_size)
        data = {
            'per_days': days_amounts_sorted,
            'count': num_records,
            'num_pages': num_pages,
            'for_period': {
                **amounts_for_period,
                'period': f'{date_from:%d.%m.%Y}-{date_until:%d.%m.%Y}'
                }
        }

        return Response(data)
