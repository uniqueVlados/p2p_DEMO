from loguru import logger
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import BaseUserManager

from utils import send_service_mail
from .utils import get_password


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('Email must be set.'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if not password:
            password = get_password()

        user_role = None if not user.role else user.role.name
        user.set_password(password)
        user.save()
        logger.info(f'Пользователь {user} создан.')
        match user_role:
            case 'Партнёр' | 'Оператор' | 'Администратор':
                email = user.email
                subject = 'Данные для входа'
                message = f'Данные для входа. Логин - ваша почта, пароль {password}'
                send_service_mail(
                    email=email,
                    subject=subject,
                    message=message
                    )
                logger.info(f'Пользователю {user} отправлено письмо с данными для входа.')
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
