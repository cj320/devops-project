from django.urls import path
from subreddits.views import subreddit_form_view, index_view, post_index_view, SubredditViews
app_name = 'subreddits'
urlpatterns = [
    path('', subreddit_form_view, name='get-subreddit'),
    path('content/', index_view, name='index-view'),
    path('content/<int:id>/', post_index_view, name='post-index'),
    path('api/subreddit/', SubredditViews.as_view(), name='sub-view'),
    path('api/subreddit/<int:id>/', SubredditViews.as_view(), name='sub-view-detail'),
]

