# Generated by Django 4.1.7 on 2023-02-22 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reua', '0008_remove_foundingdocument_icon_foundingdocument_kind_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Назва (українською)')),
                ('title_en', models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='Назва (англійською)')),
            ],
            options={
                'verbose_name': 'Категорія компаній',
                'verbose_name_plural': 'Категорії компаній',
                'ordering': ['id'],
            },
        ),
    ]
