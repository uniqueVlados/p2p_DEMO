import random

from constance import config
from itertools import (
    groupby,
    islice,
    )
import random

from loguru import logger
from typing import (
    Optional,
    Tuple,
    )

from django.conf import settings
from django.db import transaction
from django.db.models import Count, Q

from qiwi.services import update_qiwi_account_turnover
from users.models import User

from .models import (
    Account,
    Payroll,
    Card,
    Bank,
    )


def create_account(user) -> Account:
    '''Создать счёт пользователя.

    params:
    user: User
    '''
    account = Account(
        user=user,
        )
    account.save()
    logger.info(f'Создан счёт для партнёра {user}')
    return account


def update_system_balance(amount: float) -> bool:
    '''Обновить баланс системы (комиссий)'''
    account = Account.objects.get(id=settings.SYSTEM_ACCOUNT_ID)
    current_balance = account.balance
    account.balance = current_balance + amount
    account.save()
    return True


def update_partner_balance(payroll: Payroll):
    '''Обновить баланс партнера'''
    partner = payroll.partner
    account = partner.account
    current_balance = account.balance
    amount = payroll.amount
    comission_amount = payroll.comission_amount
    with transaction.atomic():
        if payroll.payment_type == Payroll.PaymentTypes.REPLENISHMENT.value:
            account.balance = current_balance + amount - comission_amount
        if payroll.payment_type == Payroll.PaymentTypes.WITHDRAWL.value:
            account.balance = current_balance - amount - comission_amount
        account.save()
        update_system_balance(comission_amount)
        payroll.performed = True
        payroll.save()


def update_card_turnover(payroll: Payroll):
    '''Обновить оборот карты'''
    card_number = payroll.card_number
    card = Card.objects.get(number=card_number)
    current_turnover = card.current_turnover
    card.current_turnover = current_turnover + payroll.amount
    card.save()


def update_tool_turnover(payroll: Payroll):
    '''Обновить оборот карты или счета в зависимости от банка'''
    if payroll.bank.slug == 'qiwi':
        update_qiwi_account_turnover(payroll)
    else:
        update_card_turnover(payroll)


def handle_failed_payroll(payroll: Payroll):
    '''Обработать отклонённое платежное поручение'''
    payroll.performed = True
    payroll.save()


def create_payroll(
        partner: User = None,
        payment_type: Payroll.PaymentTypes = None,
        operator: User = None,
        card_number: int = None,
        amount: float = None,
        back_url: str = '',
        ) -> Payroll:
    comission_amount = config.COMISSION * amount
    remittance_amount = amount - comission_amount
    payroll = Payroll(
        partner=partner,
        payment_type=payment_type,
        operator=operator,
        card_number=card_number,
        amount=amount,
        remittance_amount=remittance_amount,
        comission_amount=comission_amount,
        back_url=back_url,
        )
    payroll.save()
    return payroll


def select_card(
        amount: float,
        operator: User = None,
        bank: Bank = None
        ) -> Optional[Card]:
    '''Выбрать банковскую карту для проведения операции.'''

    turnover_limit = settings.CARD_TURNOVER_LIMIT
    current_limit = turnover_limit - amount

    cards = Card.objects.filter(
        is_active=True,
        current_turnover__lt=current_limit,
        bank=bank,
    )
    ids = list(cards.values_list('id', flat=True))
    random_id = random.choice(ids)
    random_card = Card.objects.get(id=random_id)
    return random_card


def select_operator() -> User:
    '''Выбрать оператора для проведения операции.'''
    operators_active = list(
        User.objects.filter(
            role__name='Оператор',
            is_active=True
        ).annotate(
            num_payrolls=Count(
                'handled_payrolls',
                filter=Q(handled_payrolls__status=Payroll.Statuses.NEW.value))
            ).values_list('num_payrolls', 'pk')
            )
    operators_active = sorted(operators_active, key=lambda x: x[0])
    operators_active_grouped = groupby(operators_active, key=lambda x: x[0])
    for num_payrolls, ids in islice(operators_active_grouped, 1):
        operators_active_with_min_payrolls = [x[1] for x in ids]
    selected_id = random.choice(operators_active_with_min_payrolls)
    operator = User.objects.get(id=selected_id)

    return operator


def select_operator_and_card(
        amount: float,
        bank: Bank = None
        ) -> Tuple[Optional[User], Optional[Card]]:
    '''Выбрать оператора и карту для проведения операции.'''
    turnover_limit = settings.CARD_TURNOVER_LIMIT
    current_limit = turnover_limit - amount

    filter_new_payrolls = Q(handled_payrolls__status=Payroll.Statuses.NEW)
    filter_pending_payrolls = Q(handled_payrolls__status=Payroll.Statuses.PENDING)
    filter_processing_payrolls = Q(handled_payrolls__status=Payroll.Statuses.PROCESSING)

    operators_active = list(
        User.objects.filter(
            role__name='Оператор',
            is_active=True,
            attached_cards__is_active=True,
            attached_cards__current_turnover__lt=current_limit,
            attached_cards__bank=bank,
        ).prefetch_related('attached_cards').annotate(
            num_new_payrolls=Count(
                'handled_payrolls',
                filter=filter_new_payrolls | filter_pending_payrolls | filter_processing_payrolls,
                distinct=True,
                )
            ).values_list('num_new_payrolls', 'pk')
            )
    if not operators_active:
        return (None, None)

    operators_active = sorted(operators_active, key=lambda x: x[0])
    logger.info(f'{operators_active=}')
    selected_id = operators_active[0][1]
    operator = User.objects.get(id=selected_id)

    cards = Card.objects.filter(
        is_active=True,
        current_turnover__lt=current_limit,
        bank=bank,
        operator=operator,
        )
    ids = list(cards.values_list('id', flat=True))
    random_id = random.choice(ids)
    random_card = Card.objects.get(id=random_id)
    logger.info(f'Выбраны {operator=} и {random_card=}')

    return operator, random_card


def get_payroll_by_uid(uid: str) -> Optional[Payroll]:
    try:
        payroll = Payroll.objects.get(uid=uid)
    except Payroll.DoesNotExist:
        return None
    return payroll
