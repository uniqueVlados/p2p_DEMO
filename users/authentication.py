
from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed


class ExpiringTokenAuthentication(TokenAuthentication):
    '''Аутентификация с ограниченным по времени жизни токеном.'''
    def is_token_expired(self, token) -> bool:
        return timezone.now() - token.created > timedelta(hours=settings.TOKEN_EXPIRED_AFTER_HOURS)

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise AuthenticationFailed(_('Invalid token.'))

        if not token.user.is_active:
            raise AuthenticationFailed(_('User inactive or deleted.'))

        if self.is_token_expired(token):
            raise AuthenticationFailed(_('Token is expired.'))

        return (token.user, token)


token_auth = ExpiringTokenAuthentication()
