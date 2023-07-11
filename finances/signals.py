from django_eventstream import send_event
from loguru import logger

from django.db.models.signals import post_save
from django.dispatch import receiver

# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
# from webpush import send_user_notification
# from django.contrib.auth.models import User
from .models import Payroll
from .services import (
    update_partner_balance,
    handle_failed_payroll,
    update_tool_turnover,
    )


@receiver(post_save, sender=Payroll)
def notification_handler(sender, instance, created, **kwargs):
    '''Отправить уведомление'''
    _ = (sender, instance, created, kwargs)
    if instance.performed:
        return
    
    # Если платеж через QIWI, то оператор не уведомляется
    if instance.bank:
        slug_name = instance.bank.slug
    else:
        slug_name = ''
    if instance.status == Payroll.Statuses.PROCESSING.value and slug_name != 'qiwi':
        num = str(instance.card_number)
        send_event(
            "payrolls",
            "message",
            {
                "operator_id": instance.operator.id,
                "amount": float(instance.remittance_amount),
                "card": "{}-{}-{}-{}".format(num[:4], num[4:8], num[8:12], num[12:]),
                        }
        )
        logger.info(f'Отправлено уведомление {instance.uid}, оператор {instance.operator}')


@receiver(post_save, sender=Payroll)
def handle_completed_payment(sender, instance, created, **kwargs):
    '''Отправить уведомление'''
    _ = (sender, instance, created, kwargs)
    if instance.performed:
        return
    
    if instance.status == Payroll.Statuses.APPROVED.value:
        update_partner_balance(instance)
        if instance.payment_type == Payroll.PaymentTypes.REPLENISHMENT.value:
            update_tool_turnover(instance)

    if instance.status in [
            Payroll.Statuses.FAILED.value,
            Payroll.Statuses.REJECTED.value
            ]:
        handle_failed_payroll(instance)
