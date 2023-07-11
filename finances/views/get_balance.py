from rest_framework.generics import (
    GenericAPIView,
    )
from rest_framework.response import Response

from encryption.hmac import is_user_request_valid
from users.services import get_user_by_secret_key
from utils import error

from ..models import (
    Account
    )
from ..serializers import (
    BalanceSerializer,
    )


# TODO добавить разрешения
class BalanceRetrieveView(GenericAPIView):
    queryset = Account.objects.all()
    serializer_class = BalanceSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data,
            context={
                'request': request
                }
            )

        if not serializer.is_valid(raise_exception=True):
            return error(400, 'Ошибка валидации предоставленных данных.')

        secret_key = serializer.validated_data['secret_key']
        partner = get_user_by_secret_key(secret_key)
        if not partner:
            return error(404, 'Партнёр не найден.')

        # Проверка цифровой подписи
        request_content = request.data
        signature = request.META.get('HTTP_SIGNATURE')
        is_valid, err_response = is_user_request_valid(request_content, signature, partner)
        if not is_valid:
            return err_response

        account = partner.account
        balance = account.balance
        response = {
            "balance": float(balance),
        }

        return Response(response)

    def get(self, request):
        # убрана проверка секретного ключа для запросов из ЛК
        # secret_key = request.META.get('HTTP_SECRETKEY')
        # if not secret_key:
        #     return error(400, 'Нет ключа.')
        # partner = get_user_by_secret_key(secret_key)
        partner = request.user
        if not partner:
            return error(404, 'Партнёр не найден.')

        account = partner.account
        balance = account.balance
        response = {
            "balance": float(balance),
        }

        return Response(response)
