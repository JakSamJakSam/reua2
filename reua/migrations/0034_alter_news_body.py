# Generated by Django 4.1.7 on 2023-03-24 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reua', '0033_generalprojectimages_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='body',
            field=models.TextField(blank=True, verbose_name='Зміст (українською)'),
        ),
    ]