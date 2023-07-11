from time import sleep
from loguru import logger
from rest_framework.generics import (
    GenericAPIView,
    )
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from users.services import get_user_by_secret_key
from utils import error

from ..models import (
    Payroll
    )
from ..serializers import (
    PayrollUIDSerializer,
    )
from ..services import get_payroll_by_uid


# TODO добавить разрешения
class PayrollStatusRetrieveView(ObtainAuthToken, GenericAPIView):
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
            return error(400, 'Запрос статуса: Ошибка валидации данных.')

        secret_key = request.META.get('HTTP_SECRETKEY')
        if not secret_key:
            return error(400, 'Нет ключа.')
        partner = get_user_by_secret_key(secret_key)
        if not partner:
            logger.error(f'Получить суммы и номер карты SK={secret_key[:20]}')
            return error(404, 'Партнёр не найден.')

        payroll_uid = serializer.validated_data['uid']
        payroll = get_payroll_by_uid(payroll_uid)
        if not payroll:
            sleep(5)
            return error(404, 'Платежное поручение не найдено.')

        # TODO сделать проверку на то, что пользователь системный
        # и выдавать ему баланс (для форм списания и пополнения)

        # if partner != payroll.partner:
        #     return Response(
        #         status=400,
        #         data={"error": "Автор запроса и владелец платежного поручения не совпадают."}
        #         )
        response = {
            "status": payroll.status,
        }

        return Response(response)
