# Generated by Django 3.0.7 on 2020-06-09 02:16

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20200608_1810'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='beta',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='description',
            field=models.TextField(help_text='description of company', null=True),
        ),
        migrations.AddField(
            model_name='ticker',
            name='outstanding_shares',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='control',
            name='changed_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 9, 2, 16, 35, 464814, tzinfo=utc), editable=False, verbose_name='changed_at'),
        ),
        migrations.AlterField(
            model_name='control',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 9, 2, 16, 35, 464814, tzinfo=utc), editable=False, verbose_name='created_at'),
        ),
    ]