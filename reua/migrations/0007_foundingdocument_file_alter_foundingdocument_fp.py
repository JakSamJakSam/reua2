# Generated by Django 4.1.7 on 2023-02-21 13:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flatpages', '0001_initial'),
        ('reua', '0006_foundingdocument'),
    ]

    operations = [
        migrations.AddField(
            model_name='foundingdocument',
            name='file',
            field=models.FileField(blank=True, default=None, null=True, upload_to='files', verbose_name='Файл (pdf)'),
        ),
        migrations.AlterField(
            model_name='foundingdocument',
            name='fp',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.RESTRICT, to='flatpages.flatpage', verbose_name='flat page'),
        ),
    ]