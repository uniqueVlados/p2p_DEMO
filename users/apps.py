from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        autodiscover_modules('signals')
