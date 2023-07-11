from loguru import logger
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import (
    GenericAPIView,
    )
from rest_framework.response import Response

from django.contrib.auth.models import Group

from role_permissions.models import UserRole
from users.models import (
    User,
    )
from users.serializers import UserSerializer

from ..serializers import (
    PartnerSerializer,
    )


class PartnerCreateView(ObtainAuthToken, GenericAPIView):
    queryset = User.objects.filter(role__name='Партнёр')
    serializer_class = PartnerSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data,
            context={
                'request': request
                }
            )
        if not serializer.is_valid(raise_exception=False):
            logger.error('Создание партнёра: Ошибка валидации данных.')
            return Response(
                status=400,
                data={"error": "Ошибка валидации предоставленных данных."}
                )

        # TODO перенести создание пользователя в services.py
        # Создаем пользователя, добавляем роль Партнёр и группу Партнёры
        password = User.objects.make_random_password(length=8)
        serializer.validated_data['password'] = password
        user_serializer = UserSerializer(
            data=serializer.validated_data,
            context={
                'request': request
                }
            )
        if not user_serializer.is_valid(raise_exception=False):
            return Response(
                status=400,
                data={"error": "Электронный адрес уже существует в системе."}
                )
        user = User(**user_serializer.validated_data)
        user.set_password(password)
        user.role = UserRole.objects.get(name='Партнёр')
        user.save()
        user.groups.add(Group.objects.get(name='Партнёры'))
        user.save()
        user.refresh_from_db()

        # счёт Партнёра создаётся по сигналу post_save, см. signals.py
        # секретный ключ Партнёра создаётся по сигналу post_save, см. signals.py

        secret_key = user.secret_keys.order_by('created_at').last()

        response = {
            "status": "success",
            "message": "Partner and his account have been created.",
            "secret_key": secret_key.key,
            "user_id": user.id,
            "account_id": user.account.id,
        }

        return Response(response)
