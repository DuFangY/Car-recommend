# Generated by Django 2.0.1 on 2021-04-10 05:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0007_auto_20210409_2343'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='personwebsite',
        ),
        migrations.DeleteModel(
            name='Personwebsite',
        ),
    ]
