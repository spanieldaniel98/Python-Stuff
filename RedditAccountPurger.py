import praw
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
delete_posts = True

# If you want to limit how many recent comments/posts to delete respectively, alter None to a number
# e.g. comment_limit = 10 will result in your 10 most recent comments being deleted
comment_limit = None
post_limit = None

# Don't edit below (this is where the magic happens)! 
reddit = praw.Reddit(
    user_agent=user_agent,
    client_id=client_id,
    client_secret=client_secret,
    username=username,
    password=password)

redditor = reddit.redditor(username)
    
def del_comments():
    for comment in redditor.comments.new(limit=comment_limit):
        comment.edit(".")
        comment.delete()
  
def del_posts():
    for submission in redditor.submissions.new(limit=post_limit):
        if(submission.is_self):
            submission.edit(".")
        submission.delete()

if(delete_comments):
    Thread(target=del_comments).start()
if(delete_posts):
    Thread(target=del_posts).start()