from django.test import TestCase
import unittest
from query import validate_subreddit


sub = 'gifs'
validate = validate_subreddit(sub)
assert validate == sub
