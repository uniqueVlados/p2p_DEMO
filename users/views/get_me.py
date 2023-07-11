from rest_framework.generics import (
    RetrieveAPIView,
    )

from ..models import User
from ..serializers import (
    UserSerializer,
    )


class GetMeView(RetrieveAPIView):
    '''Возвращает информацию о текущем пользователе.'''
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
