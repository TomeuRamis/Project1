# Generated by Django 2.1.4 on 2019-05-17 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0009_auto_20190430_1300'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='request',
            name='topology',
        ),
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(default=None, max_length=128),
        ),
        migrations.DeleteModel(
            name='Topology',
        ),
    ]