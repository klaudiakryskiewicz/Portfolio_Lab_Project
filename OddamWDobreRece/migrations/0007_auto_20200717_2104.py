# Generated by Django 3.0.8 on 2020-07-17 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OddamWDobreRece', '0006_auto_20200714_2238'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='is_taken',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='donation',
            name='phone_number',
            field=models.CharField(max_length=12),
        ),
        migrations.AlterField(
            model_name='donation',
            name='zip_code',
            field=models.CharField(max_length=8),
        ),
    ]
