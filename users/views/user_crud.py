from django.conf import settings
from loguru import logger
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    )
from rest_framework.response import Response

from ..models import User
from ..serializers import (
    UserSerializer,
    UserPersonDataSerializer,
    )
from utils import send_service_mail


class UserCreateView(ObtainAuthToken, CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @logger.catch
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={
                'request': request
                }
            )
        if not serializer.is_valid(raise_exception=False):
            logger.error('user_create: user exists or bad password.')
            return Response(
                status=400,
                data={"error": "Электронный адрес уже существует в системе или пароль не соответствует требования."}
                )
        password = serializer.validated_data.pop('password')
        user = User(**serializer.validated_data)
        user.set_password(password)
        user.save()
        logger.info(f'Создан пользователь {user}')
        token = Token.objects.create(user=user)

        response = {
            'success': True,
        }

        if not settings.DEBUG:
            sent_message = send_service_mail(
                email=user.email,
                subject='Confirm your email',
                endpoint='/confirm',
                token=token.key)
            if not sent_message:
                response['errors'] = 'Mail is not sent.'

        if settings.DEBUG:
            response['token'] = token.key
        return Response(response)


class UserRetrieveView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserPersonDataSerializer


class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserPersonDataSerializer
