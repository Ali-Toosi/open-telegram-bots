# Generated by Django 3.2.13 on 2022-07-16 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incomingmessagesbot', '0002_auto_20220716_2122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatwebhook',
            name='token',
            field=models.TextField(max_length=32, unique=True),
        ),
    ]