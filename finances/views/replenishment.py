from loguru import logger
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import (
    GenericAPIView,
    )
from rest_framework.response import Response

from django.conf import settings

from users.services import get_user_by_secret_key
from utils import error

from ..models import (
    Payroll,
    )
from ..serializers import (
    PayrollReplenishSerializer,
    PayrollUIDSerializer,
    )
from ..services import (
    create_payroll,
    select_operator,
    get_payroll_by_uid,
    )


# TODO добавить разрешения
class PayrollReplenishCreateView(ObtainAuthToken, GenericAPIView):
    '''Создать платежное поручение для пополнения'''
    queryset = Payroll.objects.all()
    serializer_class = PayrollReplenishSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data,
            context={
                'request': request
                }
            )
        if not serializer.is_valid(raise_exception=True):
            logger.error('Создание платежной ведомости: Ошибка валидации данных.')
            return Response(
                status=400,
                data={"error": "Ошибка валидации предоставленных данных."}
                )

        # Находим Партнёра
        secret_key = request.META.get('HTTP_SECRETKEY')
        if not secret_key:
            return error(400, 'Нет ключа.')
        partner = get_user_by_secret_key(secret_key)
        if not partner:
            logger.error(f'Получить суммы и номер карты SK={secret_key[:20]}')
            return error(400, 'Пополнение: Партнёр не найден.')

        amount = serializer.validated_data['amount']
        if amount < settings.MIN_TRANSACTION_AMOUNT:
            return error(
                400,
                f'Пополнение: Сумма транзакции меньше минимальной {settings.MIN_TRANSACTION_AMOUNT}.'
                )
        back_url = serializer.validated_data['backURL']
        operator = select_operator()

        payroll = create_payroll(
            partner=partner,
            payment_type=Payroll.PaymentTypes.REPLENISHMENT.value,
            operator=operator,
            amount=amount,
            back_url=back_url,
        )

        link_to_payment_form = settings.URL_REPLENISH + f'?uid={payroll.uid}'
        response = {
            "uid": payroll.uid,
            "amount": amount,
            "key": secret_key,
            "link": link_to_payment_form,
        }

        return Response(response)


# TODO добавить разрешения
class PayrollReplenishPayedView(ObtainAuthToken, GenericAPIView):
    '''Запрос 'Я оплатил' из сценария пополнения.'''
    queryset = Payroll.objects.all()
    serializer_class = PayrollUIDSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data,
            context={
                'request': request
                }
            )
        if not serializer.is_valid(raise_exception=True):
            return error(400, 'Обработка оплаты пользователя: UID.')

        # Находим Партнёра
        secret_key = request.META.get('HTTP_SECRETKEY')
        if not secret_key:
            return error(400, 'Нет ключа.')
        partner = get_user_by_secret_key(secret_key)
        if not partner:
            return error(400, 'Обработка оплаты пользователя: Партнёр не найден.')

        uid = serializer.validated_data['uid']
        payroll = get_payroll_by_uid(uid)
        if payroll.payment_type != Payroll.PaymentTypes.REPLENISHMENT.value:
            return error(400, 'Обработка оплаты пользователя: Неверный тип платежа.')
        payroll.status = Payroll.Statuses.PROCESSING.value
        payroll.save()

        response = {
            "status": payroll.status,
            "uid": payroll.uid,
        }

        return Response(response)
