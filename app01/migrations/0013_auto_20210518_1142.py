# Generated by Django 2.0.1 on 2021-05-18 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0012_auto_20210518_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='down_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='car_love',
            name='hot_score',
            field=models.IntegerField(default=-99999),
        ),
    ]