# Generated by Django 3.0.8 on 2020-07-14 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('description', models.TextField()),
                ('year_in_school', models.IntegerField(choices=[('1', 'Foundation'), ('2', 'Non-governmental organization'), ('3', 'Local collection')], default='1')),
                ('categories', models.ManyToManyField(to='OddamWDobreRece.Category')),
            ],
        ),
    ]
