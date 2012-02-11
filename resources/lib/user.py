import re
from ClientForm import ParseResponse
from BeautifulSoup import SoupStrainer, MinimalSoup as BeautifulSoup
import urllib2

URLPROFILE = 'http://www.ted.com/profiles/'
URLLOGIN = 'http://www.ted.com/session/new'

class User:
    """
    User identity.
    userID User ID or None if not provided / wrong.
    realName Real name or None if not provided / wrong.
    """

    def __init__(self, getHTML, username = None, password = None):
        """
        getHTML Takes a URL and optionally HTTP headers, also handles cookies.
        """
        self.getHTML = getHTML
        if username and password:
            self.userID, self.realName = self.__getUserDetails(username, password)
        else:
            self.userID = self.realName = None

    def __getUserDetails(self, username, password):
        html = self.__getLoginResponse(username, password)
        userContainer = SoupStrainer(attrs = {'class':re.compile('notices')})
        for aTag in BeautifulSoup(html, parseOnlyThese = userContainer).findAll('a'):
            if aTag['href'].startswith(URLPROFILE):
                userID = aTag['href'].split('/')[-1]
                realName = aTag.string.strip()
                return userID, realName
        return None, None

    def __getLoginResponse(self, username, password):
        # (???) clientform doesn't like HTML, and I don't want to monkey patch it
        try:
            response = urllib2.urlopen(URLLOGIN)
            forms = ParseResponse(response, backwards_compat=False)
        finally:
            response.close()
        #set username & password in the sign in form
        form = forms[1]
        form["users[username]"] = username
        form["users[password]"] = password
        form["users[rememberme]"] = ["on"]
        #click submit
        return self.getHTML(form.click())
