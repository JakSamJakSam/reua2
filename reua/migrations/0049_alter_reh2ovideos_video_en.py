# Generated by Django 4.2.3 on 2023-11-10 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reua', '0048_alter_reh2ovideos_video_en'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reh2ovideos',
            name='video_en',
            field=models.FileField(blank=True, default=None, null=True, upload_to='video_en', verbose_name='Головне відео (англ.)'),
        ),
    ]
