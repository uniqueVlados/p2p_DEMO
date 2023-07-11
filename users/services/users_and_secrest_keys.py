from loguru import logger
from typing import Optional

from ..models import (
    User,
    SecretKey,
    EncryptionKey,
    )


def create_secret_key(user: User) -> SecretKey:
    secret_key = SecretKey(
        partner=user,
        )
    secret_key.save()
    logger.info(f'Создан Secret key для партнёра {user}')
    return secret_key


def create_encryption_key(user: User) -> EncryptionKey:
    encryption_key = EncryptionKey(
        partner=user,
        )
    encryption_key.save()
    logger.info(f'Создан Encryption key для партнёра {user}')
    return encryption_key


def get_user_by_secret_key(secret_key: str) -> Optional[User]:
    try:
        secret_key_keyring = SecretKey.objects.get(key=secret_key)
    except SecretKey.DoesNotExist:
        return None
    return secret_key_keyring.partner
