#!/usr/bin/python
#
# Peteris Krumins (peter@catonmat.net)
# http://www.catonmat.net  --  good coders code, great reuse
#
# Finds all comments by a user, outputs them to stdout.
#

try:    import json
except: import simplejson as json
from itertools import count
import urllib2
import socket
import time
import sys

COMMENTS_URL = "http://www.reddit.com/user/%s/comments/.json"
COMMENT_URL  = "http://www.reddit.com/comments/%(link_id)s/xyzzy/%(comment_id)s"

class Comment(object):
    """
    Encapsulates the information about a comment

    After the object has been constructed, it contains the following attrs:
    * author       - username of author
    * comment      - comment plain text
    * upvotes      - number of upvotes
    * downvotes    - number of downvotes
    * score        - upvotes-downvotes
    * time_utc     - utc time in unix tiem format
    * time_human   - human readable time
    * link_title   - link title
    * link_id      - id of the link
    * comment_id   - id of the comment
    * url          - url to the comment
    """

def get_comments(user, pages=1, print_callback=None):
    """
    Given user, gets pages of comments (25 comments per page).
    If pages is -1, gets all the comments.
    If print_callback is specified, calls it after each page.
    """
    if print_callback is None:
        print_callback = lambda x: None

    base_url = comment_url = COMMENTS_URL % user

    comments = []
    for page_nr in count(1):
        if page_nr > pages and pages != -1:
            break
        print_callback(page_nr)
        comment_page = get_page(comment_url)
        comments.extend(extract_comments(comment_page))
        comment_url  = get_next_page_url(comment_page, base_url)
        if not comment_url: break
    return comments

def extract_comments(comment_page):
    """
    Given a JSON comment page, constructs Comment object for each comment and
    returns a list of them.
    """
    comments = []
    comment_struct = json.loads(comment_page)
    items = comment_struct['data']['children']
    for item in items:
        data = item['data']
        comment = Comment()
        comment.author      = data['author']
        comment.comment     = data['body']
        comment.time_utc    = data['created_utc']
        comment.human_utc   = time.ctime(comment.time_utc)
        comment.link_title  = data['link_title']
        comment.link_id     = data['link_id'].replace("t3_","")
        comment.comment_id  = data['name'].replace("t1_","")
        comment.upvotes     = data['ups']
        comment.downvotes   = data['downs']
        comment.score       = comment.upvotes-comment.downvotes
        comment.url         = COMMENT_URL % {
                'link_id': comment.link_id,
                'comment_id': comment.comment_id 
        }
        comments.append(comment)
    return comments

def get_next_page_url(comment_page, base_url):
    """
    Given a comment page, finds the URL to the next page.
    """
    comment_struct = json.loads(comment_page)
    after = comment_struct['data']['after']
    if after: return base_url + '?after=' + after

def get_page(url, timeout=10):
    """
    Gets and returns a web page at url with timeout 'timeout'.
    """

    old_timeout = socket.setdefaulttimeout(timeout)

    request = urllib2.Request(url)
    request.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')

    try:
        response = urllib2.urlopen(request)
        content = response.read()
    finally:
        socket.setdefaulttimeout(old_timeout)

    return content

def get_all_comments(user, print_callback):
    """ Gets all comments for user """
    return get_comments(user, -1, print_callback)

def print_comments(comments):
    """ Prints the given list of Comment objects """
    for comment in comments:
        print "Post title: " + comment.link_title.encode('utf-8')
        print "Comment date: " + comment.human_utc
        print "Comment score: %d (%d upvotes, %d downvotes)" % (
                comment.score, comment.upvotes, comment.downvotes
        )
        print "Comment URL: " + comment.url
        print 'Comment:'
        print comment.comment.encode('utf-8')
        print '-'*78
        print

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) < 2:
        print >>sys.stderr, "Usage: %s <username> [number of comment pages]" % sys.argv[0]
        sys.exit(1)

    user, pages = args
    pages = int(pages)

    def callback(page_nr):
        print >>sys.stderr, "Getting page %d of %s's comments" % (page_nr, user)

    comments = get_comments(user, pages, callback)
    print >>sys.stderr, "Got %d comments" % len(comments)
    print_comments(comments)

