# Generated by Django 3.1.1 on 2020-09-23 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('runs', '0008_auto_20200923_1741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coderackrecord',
            name='codelets_run',
            field=models.IntegerField(verbose_name='Codelets Run'),
        ),
        migrations.AlterField(
            model_name='coderackrecord',
            name='population',
            field=models.IntegerField(verbose_name='Population'),
        ),
    ]
