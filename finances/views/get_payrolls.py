from datetime import datetime
from loguru import logger
from rest_framework.generics import (
    ListAPIView,
    )
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

# from users.services import get_user_by_secret_key

from django.db.models import Q

from ..models import (
    Payroll,
    )
from ..serializers import (
    PayrollListSerializer,
    )


class PayrollsListPagination(PageNumberPagination):
    page_size = 7
    page_size_query_param = 'page_size'
    max_page_size = 10

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'results': data,
            'num_pages': self.page.paginator.num_pages,
        })


# TODO добавить разрешения
class PayrollsListView(ListAPIView):
    serializer_class = PayrollListSerializer
    pagination_class = PayrollsListPagination

    def get_queryset(self):

        # Находим Партнёра
        # secret_key = self.request.META.get('HTTP_SECRETKEY')
        # if not secret_key:
        #     return Payroll.objects.none()
        # partner = get_user_by_secret_key(secret_key)
        partner = self.request.user
        if not partner:
            logger.error('Список платежных поручений: Партнёр не найден.')
            return Payroll.objects.none()
        lookups = Q(partner=partner)
        date_from = self.request.query_params.get('date_from')
        if date_from:
            date_from = datetime.strptime(date_from, "%d.%m.%Y")
            lookups &= Q(created_at__gte=date_from)
        date_until = self.request.query_params.get('date_until')
        if date_until:
            date_until = datetime.strptime(date_until + " 23:59:59", "%d.%m.%Y %H:%M:%S")
            lookups &= Q(created_at__lte=date_until)
        payment_type = self.request.query_params.get('payment_type')
        if payment_type:
            lookups &= Q(payment_type=payment_type)
        status = self.request.query_params.get('status')
        if status:
            lookups &= Q(status=status)

        return Payroll.objects.filter(lookups).order_by('-created_at')
