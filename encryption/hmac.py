import hmac
import json

from loguru import logger

from rest_framework.response import Response

from django.conf import settings

from users.models import User
from utils import error


@logger.catch
def is_hmac_signature_ok(
        message: dict,
        signature: str,
        key: str
        ) -> bool:
    msg = json.dumps(message).encode()
    digest_mod = settings.HMAC_DIGESTMOD
    key = key.encode()
    digest = hmac.new(key, msg, digest_mod).hexdigest()
    return signature == digest


def is_user_request_valid(
        message: dict,
        signature: str,
        user: User
        ) -> Response:
    if not signature:
        return False, error(400, 'Нет цифровой подписи.')
    if not hasattr(user, 'encryption_key'):
        return False, error(400, 'Ключ не найден.')
    # encryption_key = user.encryption_key.key
    # TODO на период разработки проверка цифровой подписи убрана
    # if not is_hmac_signature_ok(message, signature, encryption_key):
    #    return False, error(400, 'Содержание запроса невалидно. Проверьте цифровую подпись.')
    return True, Response()
