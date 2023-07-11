from loguru import logger
from simple_history.admin import SimpleHistoryAdmin

from django.contrib import admin
from django.contrib.auth.models import Group

from .models import (
    User,
    )


class UserHistoryAdmin(SimpleHistoryAdmin):
    list_display = [
        'email',
        'role',
        'first_name',
        'last_name',
        'is_active',
        'is_staff',
        'confirmed',
        ]
    history_list_display = ['status']
    search_fields = ['email', ]
    list_filter = ('role', 'is_active', )
    fieldsets = (
        ('Персональные данные', {
            'fields': ('email', 'first_name', 'last_name',)
        }),
        ('Роли и статусы', {
            'fields': ('role', 'is_active', 'is_staff', 'confirmed'),
        }),
        ('Права и группы', {
            'classes': ('collapse',),
            'fields': ('groups', ),
        }),
    )

    def save_related(self, request, form, formsets, change):
        '''Сохранить M2M отношение с Group.

        Другие аттрибуты модели сохраняются по сигналу post_save,
        см. модуль signals.py.
        '''
        super(UserHistoryAdmin, self).save_related(request, form, formsets, change)
        user = form.instance
        user_role = None if not user.role else user.role.name
        match user_role:
            case 'Партнёр':
                group = Group.objects.get(name='Партнёры')
                form.instance.groups.add(group)
                logger.info(f'Пользователю {user} назначена группа прав {group}')
            case 'Оператор':
                group = Group.objects.get(name='Операторы')
                form.instance.groups.add(group)
                logger.info(f'Пользователю {user} назначена группа прав {group}')

            case'Администратор':
                group = Group.objects.get(name='Администраторы')
                form.instance.groups.add(group)
                logger.info(f'Пользователю {user} назначена группа прав {group}')

            case _:
                logger.info(f'У пользователя {user} не обнаружено известных ролей. Права не назначены.')


admin.site.register(User, UserHistoryAdmin)
