# Generated by Django 4.0.2 on 2022-02-12 11:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TwitterAuthToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oauth_token', models.CharField(max_length=255)),
                ('oauth_token_secret', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TwitterUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('twitter_id', models.CharField(max_length=255)),
                ('screen_name', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('profile_image_url', models.CharField(max_length=255, null=True)),
                ('twitter_oauth_token', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authorization.twitterauthtoken')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
