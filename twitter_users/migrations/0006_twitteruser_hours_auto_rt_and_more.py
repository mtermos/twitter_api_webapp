# Generated by Django 4.0.2 on 2022-02-27 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_users', '0005_remove_twitteruser_last_tweet_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='twitteruser',
            name='hours_auto_rt',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='twitteruser',
            name='last_auto_rt_check',
            field=models.DateTimeField(null=True),
        ),
    ]
