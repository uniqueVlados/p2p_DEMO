from loguru import logger

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from finances.services import create_account
from utils import send_service_mail

from .models import User
from .services import (
    create_secret_key,
    create_encryption_key,
    )
from .utils import get_password


@receiver(post_save, sender=User)
def create_user_attributes(sender, instance, created, **kwargs):
    '''Создать аттрибуты нового пользователя.

    Для партнёра создать счёт и секретный ключ.
    Группа прав присваивается через методы ModelAdmin (из-за M2M отношения),
    см. модуль admin.py.
    '''
    _ = (sender, instance, created, kwargs)  # исключительно для того, чтобы flake8 не орал
    user = instance
    user_role = None if not user.role else user.role.name
    if not created:
        return
    match user_role:
        case 'Партнёр':

            # Создаем счёт Партнёра
            if not hasattr(user, 'account'):
                create_account(user)
                logger.info(f'Создан счёт пользователя {user}')

            # Создаем секретный ключ Партнёра
            if not bool(user.secret_keys.all()):
                create_secret_key(user)
                logger.info(f'Создан секретный ключ пользователя {user}')

            # Создаем ключ шифрования для Партнёра
            if not hasattr(user, 'encryption_key'):
                create_encryption_key(user)
                logger.info(f'Создан ключ шифрования для пользователя {user}')


@receiver(post_save, sender=User)
def send_user_credentials(sender, instance, created, **kwargs):
    '''Отправить данные для входа
    '''
    _ = (sender, instance, created, kwargs)  # исключительно для того, чтобы flake8 не орал
    user = instance
    user_role = None if not user.role else user.role.name
    if not created:
        return
    password = get_password()
    user_role = None if not user.role else user.role.name
    user.set_password(password)
    user.save()
    logger.info(f'Пользователю {user} установлен пароль.')
    match user_role:
        case 'Партнёр' | 'Оператор' | 'Администратор':
            email = user.email
            subject = 'Данные для входа'
            message = f'Данные для входа. Логин - ваша почта, пароль {password}'
            if user_role in ['Оператор', 'Администратор']:
                message = ' '.join([message, f'Ссылка для входа: {settings.HOST}/admin/ \n'])
            is_sent = send_service_mail(
                email=email,
                subject=subject,
                message=message
                )
            if is_sent:
                logger.info(f'Пользователю {user} отправлено письмо с данными для входа.')
            else:
                logger.error(f'Ошибка отправки письма пользователю {user}.')
