# Generated by Django 2.0.1 on 2021-04-09 15:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0005_auto_20210409_2305'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='personwebsite',
        ),
    ]