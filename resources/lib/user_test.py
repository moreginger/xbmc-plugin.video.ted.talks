import unittest
from user import User
import os
import fetcher
import tempfile

class TestNewTalksRss(unittest.TestCase):
    
    def setUp(self):
        self.username = os.getenv("ted_username", None)
        self.password = os.getenv("ted_password", None)
        if (self.username == None or self.password == None):
            self.fail("Need to set ted_username and ted_password environment variables.")

    def test_login_success(self):
        cookieFile = tempfile.mkstemp()[1]
        try:
            os.remove(cookieFile)
            getHTML = fetcher.Fetcher(lambda x: cookieFile).getHTML
            user = User(getHTML, self.username, self.password)
            # Weak assertions but don't want to tie to a particular user.
            self.assertIsNotNone(user.userID)
            self.assertIsNotNone(user.realName)
        finally:
            os.remove(cookieFile)

    def test_login_failure(self):
        cookieFile = tempfile.mkstemp()[1]
        try:
            os.remove(cookieFile)
            getHTML = fetcher.Fetcher(lambda x: cookieFile).getHTML
            user = User(getHTML, self.username, self.password + "not")
            self.assertIsNone(user.userID)
            self.assertIsNone(user.realName)
        finally:
            os.remove(cookieFile)
        
    def test_no_credentials(self):
        user = User(getHTML = None) # We won't try to get any HTML
        self.assertIsNone(user.userID)
        self.assertIsNone(user.realName)
