from django.contrib import admin
from subreddits.models import Subreddit, Post
# Register your models here.
admin.site.register(Subreddit)
admin.site.register(Post)
