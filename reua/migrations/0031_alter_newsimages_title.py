# Generated by Django 4.1.7 on 2023-03-13 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reua', '0030_news_newscategory_newsimages_news_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsimages',
            name='title',
            field=models.CharField(blank=True, max_length=500, verbose_name='Заголовок (українською)'),
        ),
    ]
