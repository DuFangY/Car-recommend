# Generated by Django 2.0.1 on 2021-04-09 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_auto_20210408_2051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='img_url',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
