# Generated by Django 3.0.8 on 2020-07-14 11:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('OddamWDobreRece', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('address', models.CharField(max_length=120)),
                ('phone_number', models.IntegerField(max_length=9)),
                ('city', models.CharField(max_length=60)),
                ('zip_code', models.IntegerField(max_length=5)),
                ('pick_up_date', models.DateField()),
                ('pick_up_time', models.TimeField()),
                ('pick_up_comment', models.TextField()),
                ('categories', models.ManyToManyField(to='OddamWDobreRece.Category')),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OddamWDobreRece.Institution')),
                ('user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
