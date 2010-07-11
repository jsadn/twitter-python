
import webbrowser
import time

from api import Twitter
from oauth import OAuth, write_token_file

def oauth_dance(app_name, consumer_key, consumer_secret, token_filename=None):
    """
    Perform the OAuth dance with some command-line prompts. Return the
    oauth_token and oauth_token_secret.

    Provide the name of your app in `app_name`, your consumer_key, and
    consumer_secret. This function will open a web browser to let the
    user Allow your app to access their Twitter account. PIN
    authentication is used.

    If a token_filename is given, the oauth tokens will be written to
    the file.
    """
    print ("Hi there! We're gonna get you all set up to use %s." % app_name)
    twitter = Twitter(
        auth=OAuth('', '', consumer_key, consumer_secret),
        format='')
    oauth_token, oauth_token_secret = parse_oauth_tokens(
        twitter.oauth.request_token())
    print """
In the web browser window that opens please choose to Allow
access. Copy the PIN number that appears on the next page and paste or
type it here:
"""
    webbrowser.open(
        'http://api.twitter.com/oauth/authorize?oauth_token=' +
        oauth_token)
    time.sleep(2) # Sometimes the last command can print some
                  # crap. Wait a bit so it doesn't mess up the next
                  # prompt.
    oauth_verifier = raw_input("Please type the PIN: ").strip()
    twitter = Twitter(
        auth=OAuth(
            oauth_token, oauth_token_secret, consumer_key, consumer_secret),
        format='')
    oauth_token, oauth_token_secret = parse_oauth_tokens(
        twitter.oauth.access_token(oauth_verifier=oauth_verifier))
    if token_filename:
        write_token_file(
            token_filename, oauth_token, oauth_token_secret)
        print
        print "That's it! Your authorization keys have been written to %s." % (
            token_filename)
    return oauth_token, oauth_token_secret

def parse_oauth_tokens(result):
    for r in result.split('&'):
        k, v = r.split('=')
        if k == 'oauth_token':
            oauth_token = v
        elif k == 'oauth_token_secret':
            oauth_token_secret = v
    return oauth_token, oauth_token_secret