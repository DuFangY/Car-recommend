# Generated by Django 2.0.1 on 2021-04-10 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0008_auto_20210410_1314'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='down_count',
            field=models.IntegerField(default=0),
        ),
    ]
