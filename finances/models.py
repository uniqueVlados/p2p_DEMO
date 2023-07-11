import uuid

from constance import config
from datetime import date
from simple_history.models import HistoricalRecords

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import (
    DecimalValidator,
    MinValueValidator,
    )
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import User


class AbstractDateTimeEntity(models.Model):
    '''
    Абстрактный класс для включения полей создания и
    редактирования записи.
    '''
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Время создания'),
        )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Время редактирования'),
        )

    class Meta:
        abstract = True


class Bank(AbstractDateTimeEntity):
    '''Банк'''
    name = models.CharField(
        verbose_name=_('Название'),
        max_length=128,
        unique=True,
        )
    slug = models.SlugField(_("Кодовое название"))
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Банк')
        verbose_name_plural = _('Банки')

    def __str__(self):
        return self.name


class Card(AbstractDateTimeEntity):
    '''Банковская карта'''
    number = models.CharField(
        verbose_name=_('Номер карты'),
        max_length=48,
        unique=True,
        )
    valid_until = models.DateField(_('Действительна до'))
    bank = models.ForeignKey(
        Bank,
        on_delete=models.PROTECT,
        verbose_name='Банк',
        related_name='cards',
        null=True,
        )
    is_active = models.BooleanField(_('Активна?'), default=True)
    active_since = models.DateField(
        verbose_name=_('Активна с'),
        default=date.today,
        )
    resting_since = models.DateField(
        verbose_name=_('На паузе с'),
        null=True,
        blank=True
        )
    current_turnover = models.DecimalField(
        verbose_name=_('Текущий оборот'),
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text='оборот с момента последнего отдыха (не общий!)'
        )
    operator = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name='Оператор',
        limit_choices_to={'role': 2},  # роль Оператор
        related_name='attached_cards',
        blank=True,
        null=True,
        )
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Банковская карта')
        verbose_name_plural = _('Банковские карты')
        indexes = [
            models.Index(fields=['number', 'is_active']),
        ]

    def __str__(self):
        num = str(self.number)
        return 'Карта {}-{}-{}-{}'.format(num[:4], num[4:8], num[8:12], num[12:])

    @property
    def is_expired(self):
        return date.today > self.valid_until


class Payroll(AbstractDateTimeEntity):
    '''Платёжное поручение'''

    class Statuses(models.TextChoices):
        NEW = 'new', _('новый')
        PENDING = 'pending', _('в ожидании обработки')
        PROCESSING = 'processing', _('в обработке')
        FAILED = 'failed', _('не прошёл')
        REJECTED = 'rejected', _('отклонён')
        APPROVED = 'approved', _('одобрен')

    class PaymentTypes(models.TextChoices):
        REPLENISHMENT = 'replenishment', _('пополнение')
        WITHDRAWL = 'withdrawl', _('списание')

    uid = models.UUIDField(
        verbose_name=_("UUID"),
        editable=False,
        unique=True,
        default=uuid.uuid4,
        )
    partner = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name='Партнёр',
        limit_choices_to={'role': 3},  # роль Партнёр
        related_name='payrolls',
        )
    operator = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name='Оператор',
        limit_choices_to={'role': 2},  # роль Оператор
        related_name='handled_payrolls',
        )
    payment_type = models.CharField(
        verbose_name=_('Вид платежа'),
        max_length=32,
        choices=PaymentTypes.choices,
        )
    bank = models.ForeignKey(
        Bank,
        on_delete=models.PROTECT,
        verbose_name='Банк',
        related_name='card_payrolls',
        null=True,
        blank=True,
        )
    card_number = models.PositiveBigIntegerField(
        verbose_name=_('Номер карты'),
        blank=True,
        null=True,
        )
    account_number = models.PositiveBigIntegerField(
        verbose_name=_('Номер банковского счёта'),
        help_text=_('Для QIWI - номер телефона в формате 79119000000'),
        blank=True,
        null=True,
        )
    amount = models.DecimalField(
        _('Сумма в запросе'),
        max_digits=8,
        decimal_places=2,
        )
    remittance_amount = models.DecimalField(
        _('Сумма к переводу'),
        max_digits=8,
        decimal_places=2,
        )
    comission = models.DecimalField(
        _('Ставка комиссии'),
        max_digits=4,
        decimal_places=2,
        default=config.COMISSION
        )
    comission_amount = models.DecimalField(
        _('Сумма комиссии'),
        max_digits=8,
        decimal_places=2,
        )
    status = models.CharField(
        verbose_name=_('Статус'),
        max_length=32,
        choices=Statuses.choices,
        default=Statuses.NEW
        )
    performed = models.BooleanField(
        _('проведён?'),
        default=False,
        editable=False,
        )
    cheque = models.ImageField(
        verbose_name=_('Скан чека'),
        upload_to='uploads/%Y/%m/%d/',
        null=True,
        blank=True,
        )
    file_cheque = models.FileField(
        verbose_name=_('Документ с чеком'),
        upload_to='uploads/%Y/%m/%d/',
        null=True,
        blank=True,
        )
    back_url = models.URLField(
        verbose_name=_('URL для возврата пользователя'),
        max_length=256,
        blank=True,
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Платежное поручение')
        verbose_name_plural = _('Платежные поручения')
        permissions = [('can_handle_payroll_', _('Может проводить или отклонять платёж'))]
        indexes = [
            models.Index(fields=['operator', 'status']),
            models.Index(fields=['uid']),
            models.Index(fields=['partner']),
        ]

    def __str__(self):
        return f'Платежное поручение {self.uid}'

    # по просьбе заказчика проверка наличия чека убрана, т.е. он необязателен (13.05.2023)
    # def clean(self):
    #     is_approved = self.status == self.Statuses.APPROVED
    #     has_cheque = any([self.cheque, self.file_cheque])
    #     if is_approved and not has_cheque:
    #         raise ValidationError(
    #             _('При одобрении платежа необходимо добавить скан чека оплаты или документ.')
    #             )


class Account(AbstractDateTimeEntity):
    '''Счёт партнёра'''
    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        verbose_name='Пользователь (партнёр)',
        limit_choices_to={'role': 3},  # роль Партнёр
        related_name='account',
        )
    balance = models.DecimalField(
        verbose_name=_('Баланс'),
        default=0,
        max_digits=10,
        decimal_places=2,
        validators=[DecimalValidator(10, 2), MinValueValidator(0)],
        )

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Счёт партнёра')
        verbose_name_plural = _('Счета партнёров')

    def __str__(self):
        return f'Счёт {self.user}'
