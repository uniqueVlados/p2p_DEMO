from loguru import logger
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from ..authentication import token_auth


class Confirmation(ObtainAuthToken):
    '''Подтверждение email.'''
    def get(self, request, *args, **kwargs):
        '''
        Check token and set user.confirmed to True.
        '''
        token_key = request.GET.get('token')
        if not token_key:
            logger.error('confirmation: no token in the request.')
            return Response(status=400, data={"error": "No token in the request."})
        try:
            token = Token.objects.get(key=token_key)
        except Token.DoesNotExist:
            logger.error('confirmation: token does not exist.')
            return Response(status=400, data={"error": "Token does not exist."})
        if token_auth.is_token_expired(token):
            logger.error('confirmation: token is expired.')
            return Response(status=400, data={"error": "Token is expired."})
        user = token.user
        user.confirmed = True
        user.save()
        token.delete()
        return Response({"success": True})
