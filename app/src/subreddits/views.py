from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib import messages
import praw
import datetime

from subreddits.models import Subreddit, Post
from subreddits.serializers import SubredditSerializer, PostSerializer
from .forms import SubredditForm
from decouple import config

CLIENT_ID = config('CLIENT_ID')
CLIENT_SECRET = config('CLIENT_SECRET')
USER_AGENT = config('USER_AGENT')
REDIRECT_URI = config('REDIRECT_URI')
REFRESH_TOKEN = config('REFRESH_TOKEN')

reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT,
        redirect_uri=REDIRECT_URI,
        refresh_token=REFRESH_TOKEN
)
def convert_media(url):
    if url.endswith('.gifv'):
        l = len(url)
        url = url[:l-1]
    return url


def index_view(request):
    queryset = Subreddit.objects.all().order_by('subreddit')
    context = {'all_subs': queryset}
    return render(request,'subreddits/index.html', context)

class SubredditViews(APIView):
    def get(self, request, id=None):
        if id:
            sub = Subreddit.objects.get(id=id)
            serializer = SubredditSerializer(sub)
            return Response({"status": "success", "data": serializer.data}, status.HTTP_200_OK)
        subs = Subreddit.objects.all().order_by('subreddit')
        serializer = SubredditSerializer(subs, many=True)
        return Response({"status": "success", "data": serializer.data}, status.HTTP_200_OK)

class PostViews(APIView):
    def get(self, request, id=None):
        if id:
            post = Post.objects.get(id=id)
            serializer = PostSerializer(post)
            return Response({"status": "success", "data": serializer.data}, status.HTTP_200_OK)
        posts = PostSerializer.objects.all().order_by('subreddit')
        serializer = PostSerializer(posts, many=True)
        return Response({"status": "success", "data": serializer.data}, status.HTTP_200_OK)

def subreddit_form_view(request):
    form = SubredditForm(request.POST or None)
    if form.is_valid():
        '''
        Store Subreddit Data
        '''
        messages.success(request, 'Form submission successful')
        name = form.cleaned_data['name']
        search_by = form.cleaned_data['search_by']
        count = form.cleaned_data['number_of_submissions']
        sub = reddit.subreddit(str(name))
        image = sub.icon_img
        if not image:
            image = 'https://www.seekpng.com/png/detail/847-8478394_download-icon-reddit-svg-eps-png-psd-ai.png'
        if not Subreddit.objects.filter(subreddit=name).exists():

            description = sub.public_description
            display_name = sub.display_name
            subscribers = sub.subscribers
            slug = name
            nsfw = sub.over18

            subreddit_data = Subreddit(
                    subreddit = str(name),
                    url = str(image),
                    description = str(description),
                    display_name = str(display_name),
                    subscribers = int(subscribers),
                    nsfw = bool(nsfw),
                    slug = str(slug),
                )
            subreddit_data.save()

        if search_by == 'new':
            posts = reddit.subreddit(str(name)).new(limit=count)
        elif search_by == 'hot':
            posts = reddit.subreddit(str(name)).hot(limit=count)
        elif search_by == 'top':
            posts = reddit.subreddit(str(name)).top(limit=count)
        for post in posts:
            if Post.objects.filter(post_id=post.id).exists():
                print(f"{post.id } is exits")
                continue
            post_data = Post(
                subreddit = Subreddit.objects.get(subreddit=name),
                user = str(post.author),
                post_id = str(post.id),
                title = str(post.title),
                body = str(post.selftext),
                url = convert_media(post.url),
                permalink = str("https://reddit.com" + post.permalink),
                score = int(post.score),
                comments = int(post.num_comments),
                created = datetime.datetime.utcfromtimestamp(post.created).strftime('%Y-%m-%d %H:%M:%S'),
                slug = str(post.subreddit)
            )
            post_data.save()
    context = {'form': form}
    return render(request, "subreddits/form.html", context)

def post_index_view(request, id=id):
    data = Subreddit.objects.get(pk=id)
    all_posts = data.subreddits.all().order_by('-score')
    context = {"all_posts":all_posts}
    return render(request, "subreddits/post.html", context)

def post_detail_view(request, id):
    post = Subreddit.objects.get(id=id)
    print(post)
    context = {
        "post":post
    }
    return render(request,'subreddits/post_detail.html', context)

