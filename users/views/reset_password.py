import json

from django.conf import settings
from loguru import logger
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import (
    GenericAPIView,
    )
from rest_framework.decorators import api_view
from rest_framework.response import Response

from utils import send_service_mail, error

from ..models import User
from ..serializers import (
    PasswordSerializer,
    )
from ..utils import get_password


class ResetPasswordView(GenericAPIView):
    '''Reset password for current user.

    Check the user exists.
    Change token.
    Send email with new pass.
    '''

    @logger.catch
    def get(self, request, *args, **kwargs):
        user = self.request.user
        if not user:
            return error(404, 'Пользователь не найден.')
        # Delete current token
        token = Token.objects.filter(user=user).first()
        if token:
            token.delete()
        password = get_password()
        user.set_password(password)
        user.save()

        token = Token.objects.create(user=user)
        email = user.email
        sent_message = send_service_mail(
            email=email,
            subject='Your new password',
            message=password
            )
        logger.info(f'reset password: sent mail with new pass to {email}.')
        response = {
            'success': True,
        }
        if not sent_message:
            response['errors'] = 'Mail is not sent.'
        if settings.DEBUG:
            response['password'] = password
        return Response(response)


class ResetPasswordToken(ObtainAuthToken):
    '''Get token for password reset.

    Check the user exists.
    Get token.
    '''

    @logger.catch
    def post(self, request, *args, **kwargs):
        body = json.loads(request.body.decode())
        email = body.get('email')
        if not email:
            return Response(status=400, data={"success": False})
        logger.info(f'reset password: request from {email}.')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            logger.error('reset password: no such account.')
            return Response(
                status=404,
                data={
                    'success': False,
                    "error": "Аккаунта с таким адресом не существует",
                    })
        # Delete current token
        token = Token.objects.filter(user=user).first()
        if token:
            token.delete()

        token = Token.objects.create(user=user)
        sent_message = send_service_mail(
            email=user.email,
            subject='Reset your password',
            endpoint='/accounts/user/reset-password',
            token=token.key)
        logger.info(f'reset password: sent token mail to {email}.')
        response = {
            'success': True,
        }
        if settings.DEBUG:
            response['token'] = token.key
        if not sent_message:
            response['errors'] = 'Mail is not sent.'
        return Response(response)


@api_view(['POST'])
def reset_password(request) -> Response:
    '''
    Resets password.
    '''
    user = request.user
    serializer = PasswordSerializer(data=request.data)
    if not serializer.is_valid(raise_exception=False):
        logger.error(f'reset password: new password for {user} does not meet the requirements.')
        return Response(
            status=400,
            data={
                'success': False,
                "error": "Пароль не соответствует требованиям. Необходимо минимум 8 \
                     символов и 1 заглавная буква",
                })
    password = serializer.validated_data['password']
    user.set_password(password)
    user.save()
    token = Token.objects.get(user=user)
    token.delete()
    logger.info(f'reset password: new password for {user} is set up.')
    return Response({'success': True})
