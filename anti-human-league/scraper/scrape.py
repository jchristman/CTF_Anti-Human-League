#!/usr/bin/env python3
import praw
import pandas as pd
import datetime as dt
import sys

from config import script_id, secret, blacklist

reddit = praw.Reddit(client_id=script_id, \
                     client_secret=secret, \
                     user_agent='scraper', \
                     username='suntzu_ii', \
                     password=sys.argv[1])

subreddit = reddit.subreddit('SubredditSimulator')
top = subreddit.top('all', limit=1000)

'''
CREATE TABLE post (
	id INTEGER NOT NULL,
	title VARCHAR(256),
	text TEXT,
	post_date DATETIME,
	last_modified_date DATETIME,
	draft SMALLINT,
	PRIMARY KEY (id)
);
'''

def escape(value):
    return value.replace('"', '""')

posts = filter(
    lambda submission: submission.is_self and all(bad not in submission.title.lower() and bad not in submission.selftext.lower() for bad in blacklist),
    top
)

posts = [
    {
        'title': escape(submission.title),
        'text': escape(submission.selftext),
        'name': escape(submission.name),
        'author': submission.author,
        'created': dt.datetime.utcfromtimestamp(submission.created_utc).strftime(r'%Y-%m-%d %H:%M:%S.000000')
    }
    for submission in posts
]

# Generate SQL
for post in posts:
    print('INSERT INTO post (title, text, post_date, last_modified_date, draft) VALUES ("%s", "%s", "%s", "%s", 0);' % (post['title'], post['text'], post['created'], post['created']))


'''
CREATE TABLE user_posts (
	user_id VARCHAR(128),
	post_id INTEGER,
	CONSTRAINT uix_2 UNIQUE (user_id, post_id),
	FOREIGN KEY(post_id) REFERENCES post (id) ON DELETE CASCADE ON UPDATE CASCADE
);
'''
for i in range(len(posts)):
    print('INSERT INTO user_posts (user_id, post_id) VALUES ("testuser", %i);' % (i+1))

'''
CREATE TABLE tag (
	id INTEGER NOT NULL,
	text VARCHAR(128),
	PRIMARY KEY (id)
);
'''

print('INSERT INTO tag (text) VALUES ("DragonCTF");')

'''
CREATE TABLE tag_posts (
	tag_id INTEGER,
	post_id INTEGER,
	CONSTRAINT uix_1 UNIQUE (tag_id, post_id),
	FOREIGN KEY(tag_id) REFERENCES tag (id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY(post_id) REFERENCES post (id) ON DELETE CASCADE ON UPDATE CASCADE
);
'''

for i in range(len(posts)):
    print('INSERT INTO tag_posts (tag_id, post_id) VALUES (1, %i);' % (i+1))
