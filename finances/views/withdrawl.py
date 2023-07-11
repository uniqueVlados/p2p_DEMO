from constance import config
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
    PayrollWithdrawSerializer,
    PayrollWithdrawRequestSerializer,
    )
from ..services import (
    create_payroll,
    select_operator,
    get_payroll_by_uid,
    )


# TODO добавить разрешения
class PayrollWithdrawCreateView(ObtainAuthToken, GenericAPIView):
    queryset = Payroll.objects.all()
    serializer_class = PayrollWithdrawSerializer

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
            logger.error('Списание: Партнёр не найден.')
            return Response(
                status=404,
                data={"error": "Партнёр не найден."}
                )

        # Проверка баланса с учетом комиссии
        amount = serializer.validated_data['amount']
        if amount < settings.MIN_TRANSACTION_AMOUNT:
            return error(
                400,
                f'Пополнение: Сумма транзакции меньше минимальной {settings.MIN_TRANSACTION_AMOUNT}.'
                )

        balance = partner.account.balance
        if balance < amount * (1 + config.COMISSION):
            logger.error('Списание: Недостаточно средств.')
            return Response(
                status=400,
                data={"error": "Недостаточно средств."}
                )

        back_url = serializer.validated_data['backURL']
        operator = select_operator()

        payroll = create_payroll(
            partner=partner,
            payment_type=Payroll.PaymentTypes.WITHDRAWL.value,
            operator=operator,
            amount=amount,
            back_url=back_url,
        )

        link_to_payment_form = settings.URL_WITHDRAW + f'?uid={payroll.uid}'
        response = {
            "status": payroll.status,
            "uid": payroll.uid,
            "key": secret_key,
            "link": link_to_payment_form,
        }

        return Response(response)


# TODO добавить разрешения
class PayrollWithdrawRequestView(ObtainAuthToken, GenericAPIView):
    '''Запрос 'Ок' и ввод номера карты из сценария списания.'''
    queryset = Payroll.objects.all()
    serializer_class = PayrollWithdrawRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data,
            context={
                'request': request
                }
            )
        if not serializer.is_valid(raise_exception=True):
            return error(400, 'Обработка оплаты пользователя: UID или карта.')

        # Находим Партнёра (Системный)
        secret_key = request.META.get('HTTP_SECRETKEY')
        if not secret_key:
            return error(400, 'Нет ключа.')
        partner = get_user_by_secret_key(secret_key)
        if not partner:
            logger.error(f'Получить суммы и номер карты SK={secret_key[:20]}')
            return error(400, 'Обработка оплаты пользователя: Партнёр не найден.')

        uid = serializer.validated_data['uid']
        card_number = serializer.validated_data['card_number']
        payroll = get_payroll_by_uid(uid)
        if payroll.payment_type != Payroll.PaymentTypes.WITHDRAWL.value:
            return error(400, 'Обработка оплаты пользователя: Неверный тип платежа.')

        # TODO сделать блокировку других операций по списанию до завершения текущего списания

        # Проверка баланса партнёра еще раз, а то мало ли ...
        balance = partner.account.balance
        if balance < float(payroll.amount) * (1 + config.COMISSION):
            return error(400, 'Списание: Недостаточно средств.')

        payroll.status = Payroll.Statuses.PROCESSING.value
        payroll.card_number = card_number
        payroll.save()

        response = {
            "uid": payroll.uid,
            "amount": payroll.amount,
            "backURL": payroll.back_url,
        }

        return Response(response)
