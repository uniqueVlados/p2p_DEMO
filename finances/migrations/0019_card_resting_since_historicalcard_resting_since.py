# Generated by Django 4.1.2 on 2022-10-28 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0018_alter_account_balance_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='resting_since',
            field=models.DateField(blank=True, null=True, verbose_name='На паузе с'),
        ),
        migrations.AddField(
            model_name='historicalcard',
            name='resting_since',
            field=models.DateField(blank=True, null=True, verbose_name='На паузе с'),
        ),
    ]
