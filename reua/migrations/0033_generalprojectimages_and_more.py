# Generated by Django 4.1.7 on 2023-03-20 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reua', '0032_banktransferattributes'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeneralProjectImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.PositiveSmallIntegerField(choices=[(1, 'ReH2O'), (2, 'ReCity')], verbose_name='Тип')),
                ('position', models.PositiveSmallIntegerField(choices=[(1, 'Зверху'), (3, 'Знизу')], verbose_name='Положення')),
                ('image', models.ImageField(upload_to='')),
                ('order', models.PositiveSmallIntegerField(default=99, verbose_name='Номер за порядком')),
            ],
            options={
                'verbose_name': 'Зображення ReH2O та ReCity',
                'verbose_name_plural': 'Зображення ReH2O та ReCity',
                'ordering': ('order',),
            },
        ),
        migrations.AlterField(
            model_name='banktransferattributes',
            name='currency',
            field=models.CharField(choices=[('UAH', '₴'), ('USD', '$'), ('EUR', '€'), ('GPB', '£')], max_length=3, verbose_name='Валюта'),
        ),
        migrations.AlterField(
            model_name='project',
            name='currency',
            field=models.CharField(choices=[('UAH', '₴'), ('USD', '$'), ('EUR', '€'), ('GPB', '£')], default='USD', max_length=3, verbose_name='Валюта'),
        ),
        migrations.AlterUniqueTogether(
            name='banktransferattributes',
            unique_together={('kind', 'currency')},
        ),
    ]