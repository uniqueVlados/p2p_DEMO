import secrets
import string
import uuid


def is_password_ok(password: str) -> bool:
    """Validates password"""
    # return all([len(password) > 7, not password.islower()])
    return len(password) > 7


def get_uuid_token() -> str:
    return str(uuid.uuid4())


def get_secret_key(length: int = 128) -> str:
    '''Получить секретный ключ.

    см. https://docs.python.org/3/library/secrets.html#recipes-and-best-practices
    '''
    limited_punctiations_set = '#$%&()*+-/:;<=>?@[]^_{|}~'
    alphabet = string.ascii_letters + string.digits + limited_punctiations_set
    key = ''.join(secrets.choice(alphabet) for i in range(length))
    return key


def get_encryprion_key() -> str:
    '''Получить ключ для шифрования.'''
    return get_secret_key(length=64)


def get_password(length: int = 12) -> str:
    '''Получить пароль.

    см. https://docs.python.org/3/library/secrets.html#recipes-and-best-practices
    '''
    alphabet = string.ascii_letters + string.digits
    key = ''.join(secrets.choice(alphabet) for i in range(length))
    return key
