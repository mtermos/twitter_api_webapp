from django.db import models
from django.utils.timezone import now

# Create your models here.
class TwitterAuthToken(models.Model):
    oauth_token = models.CharField(max_length=255)
    oauth_token_secret = models.CharField(max_length=255)

    def __str__(self):
        return self.oauth_token

class TwitterDMAuthToken(models.Model):
    oauth_token = models.CharField(max_length=255)
    oauth_token_secret = models.CharField(max_length=255)

    def __str__(self):
        return self.oauth_token


class TwitterUser(models.Model):
    twitter_id = models.CharField(max_length=255)
    screen_name = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    profile_image_url = models.CharField(max_length=255, null=True)
    minutes_rt = models.IntegerField(default=-1)
    last_rm_rt_check = models.DateTimeField(null = True)
    removed_rts_count = models.IntegerField(default=0)

    hours_auto_rt = models.IntegerField(default=-1)
    last_auto_rt_check = models.DateTimeField(null = True)
    auto_rts_count = models.IntegerField(default=0)

    twitter_oauth_token = models.ForeignKey(TwitterAuthToken, on_delete=models.CASCADE, null=True)
    twitter_dm_oauth_token = models.ForeignKey(TwitterDMAuthToken, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.screen_name

class RemoveRetweetsRecords(models.Model):
    tweet_id = models.CharField(max_length=255)
    date_time = models.DateTimeField(default=now)
    user = models.ForeignKey(TwitterUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.count

class AutoRetweetRecords(models.Model):
    tweet_id = models.CharField(max_length=255)
    date_time = models.DateTimeField(default=now)
    user = models.ForeignKey(TwitterUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.count

