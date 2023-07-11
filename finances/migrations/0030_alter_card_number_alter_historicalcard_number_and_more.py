# Generated by Django 4.1.2 on 2023-05-10 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0029_historicalpayroll_file_cheque_payroll_file_cheque'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='number',
            field=models.CharField(max_length=48, unique=True, verbose_name='Номер карты'),
        ),
        migrations.AlterField(
            model_name='historicalcard',
            name='number',
            field=models.CharField(db_index=True, max_length=48, verbose_name='Номер карты'),
        ),
        migrations.AlterField(
            model_name='historicalpayroll',
            name='comission',
            field=models.DecimalField(decimal_places=2, default=0.05, max_digits=4, verbose_name='Ставка комиссии'),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='comission',
            field=models.DecimalField(decimal_places=2, default=0.05, max_digits=4, verbose_name='Ставка комиссии'),
        ),
    ]
