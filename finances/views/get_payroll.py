from loguru import logger
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import (
    GenericAPIView,
    )
from rest_framework.response import Response

from users.services import get_user_by_secret_key
from utils import error


from ..models import (
    Payroll,
    Bank,
    )
from ..serializers import (
    PayrollBankUIDSerializer,
    )
from ..services import (
    get_payroll_by_uid,
    select_operator_and_card,
    )


# TODO добавить разрешения
class PayrollGetView(ObtainAuthToken, GenericAPIView):
    '''Запрос суммы и номера карты по uid платежного поручения'''
    serializer_class = PayrollBankUIDSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data,
            context={
                'request': request
                }
            )
        if not serializer.is_valid(raise_exception=True):
            return error(400, 'Получить суммы и номер карты: Неверные UID или банк.')

        # Находим Партнёра
        secret_key = request.META.get('HTTP_SECRETKEY')
        if not secret_key:
            return error(400, 'Нет ключа.')
        partner = get_user_by_secret_key(secret_key)
        if not partner:
            logger.error(f'Получить суммы и номер карты SK={secret_key[:20]}')
            return error(400, 'Получить суммы и номер карты: Партнёр не найден.')

        uid = serializer.validated_data['uid']
        payroll = get_payroll_by_uid(uid)
        if payroll.payment_type != Payroll.PaymentTypes.REPLENISHMENT.value:
            return error(400, 'Получить суммы и номер карты: Неверный тип платежа.')
        bank_codename = serializer.validated_data['bank']
        try:
            bank = Bank.objects.get(slug=bank_codename)
        except Bank.DoesNotExist:
            return Response(
                status=404,
                data={"error": "Банк не найден."}
                )
        operator, card = select_operator_and_card(
            amount=payroll.amount,
            bank=bank
            )
        if not all([operator, card]):
            return Response(
                status=404,
                data={"error": "Подходящих карт не найдено."}
                )

        payroll.bank = bank
        payroll.card_number = card.number
        payroll.operator = operator
        payroll.save()
        num = str(payroll.card_number)

        response = {
            "amount": payroll.amount,
            "card_number": "{} {} {} {}".format(num[:4], num[4:8], num[8:12], num[12:]),
            "backURL": payroll.back_url,
        }

        return Response(response)
