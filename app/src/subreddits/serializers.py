from rest_framework import serializers
from subreddits.models import Subreddit, Post

class SubredditSerializer(serializers.ModelSerializer):
    subreddits = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Subreddit
        fields = ('__all__')

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('__all__')