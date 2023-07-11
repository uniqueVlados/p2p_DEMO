from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models import Payroll


@api_view(['GET'])
def get_payment_types(request) -> Response:
    '''Получить список типов платежного поручения.'''
    _ = request
    payment_types_class = Payroll.PaymentTypes
    payment_types = []
    for payment_type in payment_types_class.__members__.items():
        payment_types.append((payment_type[1].value, payment_type[1].label))
    return Response(payment_types)
