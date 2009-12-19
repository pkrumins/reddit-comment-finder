This is the Reddit Comment Finder program. It's written in Python and it finds
as many comments as it can for a given person on Reddit.

It was written by Peteris Krumins (peter@catonmat.net).
His blog is at http://www.catonmat.net  --  good coders code, great reuse.

The code is licensed under the GNU GPL license.

------------------------------------------------------------------------------

This program goes through all the person's Reddit comments at
http://www.reddit.com/user/<nickname>/comments/ and prints them out.

The usage is as following:

    $ ./reddit_comments.py <username> [number of comment pages]

The default is to get 1 page of comments for reddit user "username".
If you specify magic argument -1 for [number of comment pages], it will get
all the pages.

Here is an example. It gets 1 page of comments for "redditor":

    $ ./reddit_comments.py redditor

    Post title: I just guessed the password to this account. Am I bad?
    Comment date:  Thu Dec 17 17:12:20 2009
    Comment score: 24 (26 upvotes, 2 downvotes)
    Comment URL:   http://www.reddit.com/comments/afmwd/xyzzy/c0hchmq
    Comment:
    *angry glare*
    --------------------------------------------------------------------------
    ...


You may also import reddit_comments as Python module:

    >>> import reddit_comments as rc
    >>>
    >>> comments = rc.get_comments("kn0thing", 2)
    >>> len(comments)
    50
    >>> rc.print_comments(comments)
    >>> ...

This example imports "reddit_comments" module as "rc", then it calls the
get_comments() function, that takes the username and number of pages of
comments to get, and returns a list of Comment objects. Next print_comments()
function is called that prints all the comments in the format above.

Each Comment object has the following attributes:

    * author       - username of author
    * comment      - comment plain text
    * upvotes      - number of upvotes
    * downvotes    - number of downvotes
    * score        - upvotes-downvotes
    * time_utc     - utc time in unix time format
    * time_human   - human readable time
    * link_title   - link title
    * link_id      - id of the link
    * comment_id   - id of the comment
    * url          - url to the comment

You may write your own print_comments() function that, for example, would
output the comments as HTML.

------------------------------------------------------------------------------

Have fun finding your old comments. ;)

Sincerely,
Peteris Krumins
http://www.catonmat.net

