# Generated by Django 4.1.7 on 2023-02-20 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reua', '0003_partner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partner',
            name='logo',
            field=models.FileField(upload_to='partners', verbose_name='Логотип'),
        ),
    ]
