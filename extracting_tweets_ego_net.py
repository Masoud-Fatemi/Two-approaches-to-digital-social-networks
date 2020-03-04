#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 18:49:23 2019
@author: masoud
"""

import tweepy
import functions
import time
import os

total = time.time()

src = "ADDRESS TO THE DIRECTORY OF EXTRACTED EGO NET"
username = "INTERESTED USERNAME"

#connecting to the twitter API
access_token = "YOUR KEY"
access_secret = "YOUR KEY"
consumer_key = "YOUR KEY"
consumer_secret = "YOUR KEY"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, 
                 wait_on_rate_limit_notify=True, 
                 retry_count=3, retry_delay=60)


path = src+username
raw_data = functions.load_json_list(path+'/'+username+'_complete.txt')
usernames = [list(i.keys())[0] for i in raw_data]

length = len(usernames)
res = src+username+'/tweets/' 
if not os.path.exists(res):
    os.makedirs(res)

counter = 0
for name in usernames:
	    
    counter+=1
    print("\n %d/%d" %(counter, length))
    try:
        u = api.get_user(screen_name=name)
        contact = u.friends_count
        if not u.protected and not u.verified and contact<=1000:
            print("%s number of tweets: %d" %(name, api.get_user(name).statuses_count))
	            
            tweets = api.user_timeline(name,
                                    count=200,
                                    include_rts=False,
                                    tweet_mode='extended'
                                    )
	            
            all_tweets = []
            all_tweets.extend(tweets)
            if len(tweets)>0:
                oldest_id = tweets[-1].id
                while True:
                    tweets = api.user_timeline(screen_name=name, 
	                                           # 200 is the maximum allowed count
                                           count=200,
                                           include_rts = False,
                                           max_id = oldest_id - 1,
                                           tweet_mode = 'extended'
                                           )
                    if len(tweets) == 0:
	                        break
                    oldest_id = tweets[-1].id
                    all_tweets.extend(tweets)
            print('N of tweets downloaded {}'.format(len(all_tweets)))
            result = [tweet._json for idx,tweet in enumerate(all_tweets)]
            functions.write_json_lst(result, res+name+".json")
	        
        else:
            print('"""%s""" is a private/verified account or has too many contats'%(name))
    except Exception:
        pass

print("DONE")