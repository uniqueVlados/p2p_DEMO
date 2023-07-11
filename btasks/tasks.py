from celery import shared_task
from finances.models import Card

from datetime import date, timedelta
from django.conf import settings


@shared_task
def check_cards_limit():
    Card.objects.filter(
        is_active=True,
        current_turnover__gte=settings.CARD_TURNOVER_BOUNDARY_LIMIT
        ).update(
            is_active=False,
            resting_since=date.today(),
            current_turnover=0,
            )


@shared_task
def check_cards_vacation():
    date_days_ago = date.today() - timedelta(days=settings.CARD_TURNOVER_PERIOD)
    Card.objects.filter(
        is_active=False,
        valid_until__gt=date.today(),
        resting_since__lt=date_days_ago,
        ).update(
            is_active=True,
            active_since=date.today(),
            )


# TODO решить, необходимо ли удалять просроченные карты
@shared_task
def check_cards_validity_period():
    Card.objects.filter(
        is_active=True,
        valid_until__lt=date.today()
        ).update(is_active=False)
