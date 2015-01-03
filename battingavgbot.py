#! /usr/bin/env python3
import sys
import pprint as pp
import re
from twython import Twython, TwythonStreamer

CONSUMER_KEY = 'Put It Here'
CONSUMER_SECRET = 'Put It Here'
ACCESS_KEY = 'Put It Here'
ACCESS_SECRET = 'Put It Here'
twitter = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET) 


expr = r'What is my Twitter batting average?'

def compute_batting_average(username):    
    tweet_count = 0
    hits = 0
    user_timeline = twitter.get_user_timeline(screen_name=username,
                                     include_rts=0,
                                     count=200)
    min_id = min([tweet['id'] for tweet in user_timeline])
    for tweet in user_timeline:
        min_id = min_id if min_id < tweet['id'] else tweet['id']
        tweet_count = tweet_count+1
        tweet_favorites = tweet['favorite_count']
        tweet_retweets = tweet['retweet_count']
        if tweet_favorites >= 1 or tweet_retweets >= 1:
            hits = hits + 1
        tweet_favorites = 0
        tweet_retweets = 0
    while(user_timeline):
        user_timeline = twitter.get_user_timeline(screen_name=username,
                                     include_rts=0,
                                     count=200,
                                     max_id = min_id-1)
        for tweet in user_timeline:
            min_id = min_id if min_id < tweet['id'] else tweet['id']
            tweet_count = tweet_count+1
            tweet_favorites = tweet['favorite_count']
            tweet_retweets = tweet['retweet_count']
            if tweet_favorites >= 1 or tweet_retweets >= 1:
                hits = hits + 1
            tweet_favorites = 0
            tweet_retweets = 0
    try:
        average = hits/tweet_count
    except ZeroDivisionError:
        average = None
    return average

class MyStreamer(TwythonStreamer):
    def on_success(self,data):
        if 'text' in data:
            username = data['user']['screen_name']
            if username != "USER NAME OF BOT":
                if re.search(expr, data['text']):
                    print("Computing average for {0}".format(username))
                    average = compute_batting_average(username)
                    print("Average computed for {0}".format(username))
                    if average:
                        handle = "@{0} ".format(username)
                        average_str = "Your average is {0:.3}".format(average)
                        twitter.update_status(status=handle+average_str)
                    else:
                        handle = "@{0} ".format(username)
                        average_err = "Average couldn't be calculated, sorry!"
                        twitter.update_status(status=handle+average_err)
    def on_error(self, status_code, data):
       print(status_code)
       self.disconnect()

stream = MyStreamer(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)
stream.user()

