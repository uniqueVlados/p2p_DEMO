from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class FinancesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'finances'

    def ready(self):
        autodiscover_modules('signals')
