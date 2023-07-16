# Generated by Django 2.0.1 on 2021-04-09 15:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0006_remove_userinfo_personwebsite'),
    ]

    operations = [
        migrations.CreateModel(
            name='Personwebsite',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=64, verbose_name='个人主页昵称')),
                ('site_name', models.CharField(max_length=32, verbose_name='站点名称')),
                ('theme', models.CharField(max_length=32, verbose_name='个人主页主题')),
            ],
        ),
        migrations.AddField(
            model_name='userinfo',
            name='personwebsite',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.Personwebsite'),
        ),
    ]
