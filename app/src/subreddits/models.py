from django.db import models
from django.urls import reverse

class Subreddit(models.Model):
    subreddit = models.CharField(max_length=1000)
    url = models.URLField()
    description = models.TextField()
    nsfw = models.BooleanField(null=True)
    display_name = models.CharField(max_length=255)
    subscribers = models.IntegerField()
    slug = models.SlugField()
    class Meta:
        ordering = ['subreddit']

    def __str__(self):
        return f"{self.subreddit}"

class Post(models.Model):
    subreddit = models.ForeignKey(Subreddit, related_name='subreddits', on_delete=models.CASCADE)
    user = models.CharField(max_length=255)
    post_id = models.CharField(max_length=6)
    title = models.CharField(max_length=255)
    body = models.TextField(null=True)
    url = models.URLField(null=True)
    permalink = models.URLField(null=True)
    score = models.IntegerField()
    comments = models.IntegerField(null=True)
    created = models.DateTimeField()
    slug = models.SlugField(null=True)

    class Meta:
        ordering = ["subreddit", "user", "post_id", "score"]

    def __str__(self):
        return f"Subreddit: {self.subreddit} Title: {self.title}, score: {self.score}"

class PostComment(models.Model):
    comment = models.ForeignKey(Subreddit, on_delete=models.CASCADE, null=True, db_index=True)

def get_absolute_url(self):
    return reverse("subreddits:get-subreddit", kwargs={"id": self.id})
