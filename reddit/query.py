#!/usr/bin/python3
import os
import dotenv
import json
import praw
from prawcore.exceptions import ResponseException

dotenv.read_dotenv()

'''
DEFINE REDDIT PRAW ENVIRONMENT VARIABLES
'''
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
USER_AGENT = os.environ.get('USER_AGENT')
REDIRECT_URI = os.environ.get('REDIRECT_URI')
REFRESH_TOKEN = os.environ.get('REFRESH_TOKEN')

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

