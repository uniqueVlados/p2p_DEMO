from rest_framework.permissions import (
    BasePermission,
    IsAuthenticated,
    )

from .models import UserRole


class AllowOptionsAuthentication(IsAuthenticated):
    '''Класс для возрата 200_OK на запрос OPTIONS.

    По умолчанию DRF требует авторизации и для OPTIONS, возвращая 401,
    что противоречит спецификации W3C.
    '''
    def has_permission(self, request, view):
        if request.method == 'OPTIONS':
            return True
        return super().has_permission(request, view)


class IsPartnerUser(BasePermission):
    """
    Allows access only partners.
    """

    def has_permission(self, request, view):
        partner_role = UserRole.objects.get(name='Партнёр')
        return bool(request.user) and request.user.role == partner_role
