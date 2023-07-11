import json

from loguru import logger
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..authentication import token_auth


def _check_token(token_key) -> bool:
    '''Check token.'''
    if not token_key:
        return False
    try:
        token = Token.objects.get(key=token_key)
    except Token.DoesNotExist:
        return False
    if token_auth.is_token_expired(token):
        return False

    return True


@api_view(['POST'])
def check_token(request) -> Response:
    '''Handle request and return token check result.'''
    body = json.loads(request.body.decode())
    token_key = body.get('token')
    is_token_ok = _check_token(token_key)
    if not is_token_ok:
        return Response(status=404, data={"success": False})

    return Response({"success": True})


class AuthToken(ObtainAuthToken):
    '''Token Authorization.

    Check the user exists.
    Get token.
    '''

    @logger.catch
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if not serializer.is_valid(raise_exception=False):
            logger.error('auth: bad password or account.')
            return Response(
                status=400,
                data={
                    'success': False,
                    "error": "Аккаунта с таким адресом и/или паролем не существует",
                    })
        user = serializer.validated_data['user']
        if not user.confirmed:
            logger.error(f'auth: {user.email} is not yet confirmed.')
            return Response(
                status=404,
                data={
                    'success': False,
                    "error": "Email не подтвержден.",
                    })
        token, created = Token.objects.get_or_create(user=user)

        # Если токен просрочен, удалить его и создать новый
        if not created:
            is_expired = token_auth.is_token_expired(token)
            if is_expired:
                token.delete()
                token = Token.objects.create(user=user)
                logger.info(f'auth: token has been regenerated for user {user}.')

        return Response({
            'success': True,
            'token': token.key,
            'user_id': user.id,
        })
