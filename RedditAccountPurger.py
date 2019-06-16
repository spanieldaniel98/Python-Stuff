import praw
from datetime import datetime
from threading import Thread

# * This is a script written for deleting your comments and/or posts on Reddit!
# * Before running this script, on your Reddit account, go to User Settings -> Privacy & Security -> App Authorization
#   and click 'create an app...'.
# * Then give the app a name, select the 'script' radio button, and enter http://localhost:8080 as the redirect URL. 

# Edit your app details
user_agent = 'app name (above where it says "personal use script")'
client_id = '14 char key (below where it says "personal use script")'
client_secret = 'secret (27 char key)'

# Edit your account login details
username = 'your_username'
password = 'your_password'

# If you don't want to delete comments/posts, alter to False respectively
delete_comments = True
delete_posts    = True

# If you want to limit how many recent comments/posts to delete respectively, alter None to a number
# e.g. comment_limit = 10 will result in your 10 most recent comments being deleted
comment_limit = None
post_limit    = None

# If you want to skip over a number of recent comments/posts before deleting the rest, alter 0 to another number respectively
# e.g. comments_to_skip = 3 will ignore your three most recent comments and delete the rest
comments_to_skip = 0
posts_to_skip    = 0

# If you don't want to delete any comments/posts created *before* a certain date and time, edit the default date and time below
# The format is Month Day Year  Hour:Minute:Second (24 hour clock)
dont_delete_comments_before = 'January 1 1970  00:00:00'
dont_delete_posts_before    = 'January 1 1970  00:00:00'

# If you don't want to delete any comments/posts created *after* a certain date and time, edit the default date and time below
# The format is Month Day Year  Hour:Minute:Second (24 hour clock)
dont_delete_comments_after  = 'January 1 2100  00:00:00'
dont_delete_posts_after     = 'January 1 2100  00:00:00'

# Don't edit below (this is where the magic happens)! 
reddit = praw.Reddit(
    user_agent=user_agent,
    client_id=client_id,
    client_secret=client_secret,
    username=username,
    password=password)

redditor = reddit.redditor(username)

comment_before_limit = datetime.strptime(dont_delete_comments_before, '%B %d %Y %H:%M:%S')
post_before_limit    = datetime.strptime(dont_delete_posts_before   , '%B %d %Y %H:%M:%S')
comment_after_limit  = datetime.strptime(dont_delete_comments_after , '%B %d %Y %H:%M:%S')
post_after_limit     = datetime.strptime(dont_delete_posts_after    , '%B %d %Y %H:%M:%S')
    
def del_comments():
    comment_skip_counter = 0
    for comment in redditor.comments.new(limit=comment_limit):
        if(comment_skip_counter < comments_to_skip):
            comment_skip_counter += 1
        else:
            if(comment_before_limit < datetime.fromtimestamp(comment.created) < comment_after_limit):
                comment.edit(".")
                comment.delete()
  
def del_posts():
    post_skip_counter = 0
    for submission in redditor.submissions.new(limit=post_limit):
        if(post_skip_counter < posts_to_skip):
            post_skip_counter += 1
        else:
            if(post_before_limit < datetime.fromtimestamp(submission.created) < post_after_limit):
                if(submission.is_self):
                    submission.edit(".")
                submission.delete()

if(delete_comments):
    Thread(target=del_comments).start()
if(delete_posts):
    Thread(target=del_posts).start()