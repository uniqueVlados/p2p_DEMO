# Generated by Django 4.1.2 on 2022-10-23 10:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('finances', '0012_historicalpayroll_remittance_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='user',
            field=models.OneToOneField(limit_choices_to={'role': 3}, on_delete=django.db.models.deletion.PROTECT, related_name='account', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь (партнёр)'),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='operator',
            field=models.ForeignKey(limit_choices_to={'role': 2}, on_delete=django.db.models.deletion.PROTECT, related_name='handled_payrolls', to=settings.AUTH_USER_MODEL, verbose_name='Оператор'),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='partner',
            field=models.ForeignKey(limit_choices_to={'role': 3}, on_delete=django.db.models.deletion.PROTECT, related_name='payrolls', to=settings.AUTH_USER_MODEL, verbose_name='Партнёр'),
        ),
    ]