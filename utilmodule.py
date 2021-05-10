# UTILITY MODULE

import os
import json
import praw

# lambda function to flatten certain statistics
flatten = lambda n: 1 if n > 0 else 0

# extension organizer
def format_cogs():
    cogs = []
    # loading the cogs as extensions
    for filename in os.listdir('./cogs'):
        # checking type
        if filename.endswith('.py'):
            # removes '.py'
            cogs.append(f'cogs.{filename[:-3]}')

    return cogs

# more secure way to use the praw credentials
def praw_object():
    with open("praw_config.json") as f:
        creds = json.load(f)

    reddit = praw.Reddit(client_id = creds['client_id'],
                         client_secret = creds['client_secret'],
                         password = creds['password'],
                         user_agent = creds['user_agent'],
                         username = creds['username']
                        )

    return reddit

