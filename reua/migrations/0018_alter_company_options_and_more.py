# Generated by Django 4.1.7 on 2023-02-28 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reua', '0017_alter_staff_options_staff_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'ordering': ['order'], 'verbose_name': 'Компанія', 'verbose_name_plural': 'Компанії'},
        ),
        migrations.AlterModelOptions(
            name='investitioncompany',
            options={'ordering': ['order'], 'verbose_name': 'Компанія (інвестиція)', 'verbose_name_plural': 'Компанії (інвестиція)'},
        ),
        migrations.AddField(
            model_name='company',
            name='order',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Номер за порядком'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='investitioncompany',
            name='order',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Номер за порядком'),
            preserve_default=False,
        ),
        migrations.RunSQL('update reua_company set "order"=id', reverse_sql=migrations.RunSQL.noop),
        migrations.RunSQL('update reua_investitioncompany set "order"=id', reverse_sql=migrations.RunSQL.noop),
    ]
