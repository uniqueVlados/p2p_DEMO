# Generated by Django 4.1.2 on 2022-10-17 20:22

from django.contrib.auth.models import (
    Group,
    Permission,
    )
from django.contrib.contenttypes.models import ContentType
from django.db import migrations


def generate_groups(apps, schema_editor):
    '''Создает группы прав для основных действующих лиц.'''

    group_names = [
        'Администраторы',
        'Операторы',
        'Партнёры',
    ]
    for name in group_names:
        group = Group(name=name)
        group.save()
        if name == 'Администраторы':
            content_types = ContentType.objects.filter(app_label='users')
            permissions = Permission.objects.filter(content_type__in=content_types)
            group.permissions.set(permissions)


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(generate_groups),
    ]