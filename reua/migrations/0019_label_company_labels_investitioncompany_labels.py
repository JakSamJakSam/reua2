# Generated by Django 4.1.7 on 2023-03-01 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reua', '0018_alter_company_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Назва')),
                ('html_code', models.TextField(verbose_name='Код HTML (укр)')),
                ('html_code_en', models.TextField(blank=True, verbose_name='Код HTML (aнгл)')),
                ('order', models.PositiveSmallIntegerField(verbose_name='Номер за порядком')),
            ],
            options={
                'verbose_name': 'Мітка  компанії',
                'verbose_name_plural': 'Мітки компаній',
                'ordering': ['order'],
            },
        ),
        migrations.AddField(
            model_name='company',
            name='labels',
            field=models.ManyToManyField(to='reua.label', verbose_name='Мітки'),
        ),
        migrations.AddField(
            model_name='investitioncompany',
            name='labels',
            field=models.ManyToManyField(to='reua.label', verbose_name='Мітки'),
        ),
    ]