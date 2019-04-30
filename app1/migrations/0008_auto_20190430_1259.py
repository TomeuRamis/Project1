# Generated by Django 2.1.4 on 2019-04-30 12:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0007_auto_20181214_2027'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topology',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attribute1', models.IntegerField(choices=[('a1', 1), ('a2', 2), ('a3', 3)])),
                ('attribute2', models.CharField(choices=[('b1', 'a'), ('b2', 'b'), ('b3', 'c')], default='b1', max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='request',
            name='time',
            field=models.DurationField(default=None),
        ),
        migrations.AlterField(
            model_name='request',
            name='status',
            field=models.CharField(choices=[('P', 'pending'), ('S', 'started'), ('F', 'finished')], default='P', max_length=1),
        ),
        migrations.AddField(
            model_name='request',
            name='topology',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='app1.Topology'),
            preserve_default=False,
        ),
    ]