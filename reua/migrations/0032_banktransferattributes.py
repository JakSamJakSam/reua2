# Generated by Django 4.1.7 on 2023-03-17 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reua', '0031_alter_newsimages_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankTransferAttributes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.PositiveSmallIntegerField(choices=[(1, 'ReH2O'), (2, 'ReCity')], verbose_name='Тип')),
                ('currency', models.CharField(choices=[('EUR', '€'), ('USD', '$'), ('UAH', '₴')], max_length=3, verbose_name='Валюта')),
                ('attr', models.TextField(verbose_name='Банківські реквізити (укр)')),
                ('attr_en', models.TextField(blank=True, verbose_name='Банківські реквізити (англ)')),
            ],
            options={
                'verbose_name': 'Банківські реквізити',
                'verbose_name_plural': 'Банківські реквізити',
            },
        ),
    ]