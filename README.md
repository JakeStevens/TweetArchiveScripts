TweetArchiveScripts
===================

Python scripts that offers some quick looks into Twitter data

analyzetwitter.py

================

Depends on matplotlib

This uses the tweet archive. To use, place this file in the same 

location as tweets.csv and edit analyzetwitter.py to call the 

method that analyzes whatever you would like.

battingavgbot.py

=================

Depends on Twython

This requires a Twitter application. It includeds a method called

compute_batting_average that takes a username and returns the

twitter batting average (favorited or retweeted tweets / total)

for the past 3200 tweets. This method is used by a small bot that

responds to the prompt "What is my Twitter batting average"
