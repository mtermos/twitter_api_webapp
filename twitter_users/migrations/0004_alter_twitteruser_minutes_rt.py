# Generated by Django 4.0.2 on 2022-02-18 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_users', '0003_twitteruser_minutes_rt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twitteruser',
            name='minutes_rt',
            field=models.IntegerField(default=-1),
        ),
    ]
