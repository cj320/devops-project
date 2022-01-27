import os
import json
import praw
from prawcore.exceptions import ResponseException
import time
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

def validate_subreddit(sub):
    try:
        reddit.subreddits.search_by_name(sub, exact=True)
        return sub
    except ResponseException:
        print("This subreddit does not exist")

