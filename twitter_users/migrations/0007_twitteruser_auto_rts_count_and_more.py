# Generated by Django 4.0.3 on 2022-03-05 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_users', '0006_twitteruser_hours_auto_rt_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='twitteruser',
            name='auto_rts_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='twitteruser',
            name='removed_rts_count',
            field=models.IntegerField(default=0),
        ),
    ]
