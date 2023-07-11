# Generated by Django 4.1.2 on 2022-10-19 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0008_alter_payroll_options_alter_historicalpayroll_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalpayroll',
            name='status',
            field=models.CharField(
                choices=[
                    ('new', 'новый'), ('pending', 'в ожидании обработки'), ('processing', 'в обработке'), ('failed', 'не прошёл'), ('rejected', 'отклонён'), ('approved', 'одобрен')
                    ], default='new', max_length=32, verbose_name='Статус'
                ),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='status',
            field=models.CharField(choices=[
                ('new', 'новый'), ('pending', 'в ожидании обработки'), ('processing', 'в обработке'), ('failed', 'не прошёл'), ('rejected', 'отклонён'), ('approved', 'одобрен')
                ], default='new', max_length=32, verbose_name='Статус'),
        ),
    ]
