# Generated by Django 2.1.4 on 2019-05-24 12:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0020_auto_20190524_1214'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='request',
            name='date_of_finish',
        ),
        migrations.RemoveField(
            model_name='request',
            name='date_of_start',
        ),
    ]
