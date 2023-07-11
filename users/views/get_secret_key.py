from loguru import logger
from rest_framework.generics import (
    GenericAPIView,
    )
from rest_framework.response import Response

from ..models import (
    SecretKey,
    )
from ..permissions import IsPartnerUser

from ..serializers import (
    SecretKeyRetrieveSerializer,
    )


# TODO добавить разрешения
class SecretKeyRetrieveView(GenericAPIView):
    queryset = SecretKey.objects.all()
    serializer_class = SecretKeyRetrieveSerializer
    permission_classes = [IsPartnerUser]

    def get(self, request):
        user = request.user
        secret_key = user.secret_keys.order_by('created_at').last()
        logger.info(f'Пользователю {user=} выслан секретный ключ по запросу.')
        response = {
            "secret_key": secret_key.key,
        }

        return Response(response)
