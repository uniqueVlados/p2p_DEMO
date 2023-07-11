from simple_history.models import HistoricalRecords

from django.contrib.auth.models import (
    AbstractUser,
    )
from django.db import models
from django.utils.translation import gettext_lazy as _

from role_permissions.models.user_role_group import UserRole

from .managers import UserManager
from .utils import (
    get_secret_key,
    get_encryprion_key,
    )


class User(AbstractUser):
    '''
    Модель пользователя.

    Аттрибуты пользователя, вкл. groups, создаются автоматически
    по сигналу post_save, см. signals.py.
    '''
    objects = UserManager()

    username = None
    email = models.EmailField(_('email address'), unique=True)

    confirmed = models.BooleanField(
        _('Подтверждён?'),
        default=False
    )
    role = models.ForeignKey(
        UserRole,
        on_delete=models.PROTECT,
        verbose_name='Роль пользователя',
        null=True,
        blank=True,
        )
    history = HistoricalRecords()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role']),
        ]

    def __str__(self):
        return self.email

    @property
    def token(self):
        try:
            return self.auth_token
        except models.ObjectDoesNotExist:
            return None


class SecretKey(models.Model):
    '''Секретный ключ для партнёра.

    Генерируется при создании партнёра.
    Могут быть сгенерированы дополнительные ключи (см. работа с API).
    Не выводится в админке.
    '''
    name = models.CharField(
        verbose_name=_('Название'),
        max_length=32,
        )
    partner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь (партнёр)',
        limit_choices_to={'role': 3},  # роль Партнёр
        related_name='secret_keys',
        )
    key = models.CharField(
        verbose_name=_('Ключ'),
        max_length=128,
        editable=False,
        unique=True,
        default=get_secret_key,
        )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Время создания'),
        )
    is_available = models.BooleanField(
        verbose_name=_('Доступен?'),
        default=True,
        )

    class Meta:
        indexes = [
            models.Index(fields=['partner']),
        ]


class EncryptionKey(models.Model):
    '''Ключ шифрования для партнёра.

    Генерируется при создании партнёра.
    Могут быть сгенерированы дополнительные ключи (см. работа с API).
    Не выводится в админке.
    '''
    partner = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь (партнёр)',
        limit_choices_to={'role': 3},  # роль Партнёр
        related_name='encryption_key',
        )
    key = models.CharField(
        verbose_name=_('Ключ'),
        max_length=64,
        editable=False,
        unique=True,
        default=get_encryprion_key,
        )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Время создания'),
        )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Время редактирования'),
        )
    history = HistoricalRecords()

    class Meta:
        indexes = [
            models.Index(fields=['partner']),
        ]
