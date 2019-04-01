# Generated by Django 2.1.5 on 2019-04-01 14:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gas_mileages', '0002_gasmileage_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gasmileage',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='uuid'),
        ),
    ]
