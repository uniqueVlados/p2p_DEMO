from loguru import logger
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    CreateAPIView,
    DestroyAPIView,
    )
from rest_framework.response import Response

from django.db.models import Q

from utils import error

from ..models import (
    SecretKey,
    )
from ..serializers import (
    SecretKeysListSerializer,
    SecretKeySerializer,
    SecretKeyGetSerializer,
    SecretKeyCreateSerializer,
    )


# TODO добавить разрешения
class SecretKeysListView(ListAPIView):
    serializer_class = SecretKeysListSerializer

    def get_queryset(self):

        partner = self.request.user
        lookups = Q(partner=partner)

        return SecretKey.objects.filter(lookups).order_by('-created_at')


class SecretKeyGetView(RetrieveAPIView):
    serializer_class = SecretKeyGetSerializer
    queryset = SecretKey.objects.all()

    def get_queryset(self):

        partner = self.request.user
        lookups = Q(partner=partner)

        return SecretKey.objects.filter(lookups)


class SecretKeyUpdateView(UpdateAPIView):
    serializer_class = SecretKeySerializer
    queryset = SecretKey.objects.all()

    def get_queryset(self):

        partner = self.request.user
        lookups = Q(partner=partner)

        return SecretKey.objects.filter(lookups)


class SecretKeyDeleteView(DestroyAPIView):
    serializer_class = SecretKeySerializer
    queryset = SecretKey.objects.all()

    def get_queryset(self):

        partner = self.request.user
        lookups = Q(partner=partner)
        logger.info(f'{partner} удалил секретный ключ.')

        return SecretKey.objects.filter(lookups)


class SecretKeyCreateView(CreateAPIView):
    serializer_class = SecretKeyCreateSerializer
    queryset = SecretKey.objects.all()

    def post(self, request):
        partner = request.user
        serializer = self.serializer_class(
            data=request.data,
            context={
                'request': request
                }
            )
        if not serializer.is_valid(raise_exception=True):
            return error(400, 'SecretKeyCreateView: Ошибка валидации предоставленных данных.')

        name = serializer.validated_data['name']
        secret_key = SecretKey(
            name=name,
            partner=partner,
            )
        secret_key.save()
        response = {
            "success": True
        }

        return Response(response)
