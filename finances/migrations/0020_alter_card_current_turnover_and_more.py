# Generated by Django 4.1.2 on 2022-10-28 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0019_card_resting_since_historicalcard_resting_since'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='current_turnover',
            field=models.DecimalField(decimal_places=2, default=0, help_text='оборот с момента последнего отдыха (не общий!)', max_digits=10, verbose_name='Текущий оборот'),
        ),
        migrations.AlterField(
            model_name='historicalcard',
            name='current_turnover',
            field=models.DecimalField(decimal_places=2, default=0, help_text='оборот с момента последнего отдыха (не общий!)', max_digits=10, verbose_name='Текущий оборот'),
        ),
    ]
