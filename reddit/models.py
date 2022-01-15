from django.db import models

# Create your models here.
'''
This Model is is used to store Reddit user information
'''
class Posts(models.Model):
    user = models.CharField(max_length=255)
    post_id = models.CharField(max_length=6)
    subreddit = models.CharField(max_length=255)
    title = models.CharField(max_length=1000)
    body = models.TextField(blank=True, null=True)
    url = models.URLField(max_length=200)
    score = models.IntegerField()
    total_comments = models.IntegerField(null=True)
    created_at = models.DateTimeField()

    def __str__(self):
        return self.title