# Generated by Django 4.2.7 on 2023-12-06 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reua', '0056_sitesettings_recity_text_sitesettings_recity_text_en_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesettings',
            name='reCity_text_en',
            field=models.TextField(blank=True, verbose_name='Текст призначення для ReCity (англ.)'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='reh2o_text_en',
            field=models.TextField(blank=True, verbose_name='Текст призначення для ReH2O (англ.)'),
        ),
    ]