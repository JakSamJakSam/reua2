# Generated by Django 4.2.3 on 2023-11-06 15:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('reua', '0040_sitesettings_phone2'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReH2OVideos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Назва')),
                ('video', models.FileField(upload_to='video', verbose_name='Головне відео')),
                ('video_en', models.FileField(null=True, upload_to='video_en', verbose_name='Головне відео')),
                ('order', models.PositiveSmallIntegerField(default=99, verbose_name='Номер за порядком')),
            ],
            options={
                'verbose_name': 'Відео',
                'verbose_name_plural': 'Відео',
            },
        ),
        migrations.CreateModel(
            name='ReH2OSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, to='sites.site', verbose_name='Сайт')),
                ('video', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reua.reh2ovideos')),
            ],
            options={
                'verbose_name': 'Налаштування сторінки ReH2O',
                'verbose_name_plural': 'Налаштування сторінки ReH2O',
            },
        ),
    ]
