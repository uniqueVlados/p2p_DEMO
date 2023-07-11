from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models import Payroll


@api_view(['GET'])
def get_payroll_statuses(request) -> Response:
    '''Получить список возможных статусов платежного поручения.'''
    _ = request
    statuses_class = Payroll.Statuses
    statuses = []
    for status in statuses_class.__members__.items():
        statuses.append((status[1].value, status[1].label))
    return Response(statuses)
