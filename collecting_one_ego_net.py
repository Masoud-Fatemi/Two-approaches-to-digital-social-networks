#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 12:51:09 2019
@author: masoud
"""

import tweepy
import time
import functions
import os

save = True
res_dir = 'RESULT DIRECTORY'

#insert username of the interested account
username='INTERESTED ACCOUNT'
data = []
usernames = []
ids = []


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


u = api.get_user(screen_name=username)
contact = u.friends_count

#checking if it is a proper account or not
#not protected accounts, not verified accounts and the ones with <= 1000 friends
if not u.protected and not u.verified and contact<=1000:
		
	##extracting friends' usernames and ids
	print("extracting friends...")
	fr_usernames = []
	fr_ids = []
	cursor = tweepy.Cursor(api.friends, screen_name=username)
	for item in cursor.items():
	    fr_usernames.append(item.screen_name)
	    u = api.get_user(screen_name=item.screen_name)
	    fr_ids.append(u.id)

	usernames.extend([i for i in fr_usernames if i not in usernames])
	ids.extend([i for i in fr_ids if i not in ids])

	counter = 0
	for name in usernames:
	    temp = {}
	    fr = []
	    
	    try:
	        u = api.get_user(screen_name=name)
	        contact = u.friends_count
	        if not u.protected and not u.verified and contact<=1000:    
	            
	            cursor = tweepy.Cursor(api.friends_ids, screen_name=name)
	            for page in cursor.pages():
	                fr.extend(page)
	                time.sleep(20)

	            temp['friends'] = fr
	            
	            data.append({name:temp})
	            counter+=1
	            print('%d/%d \t %s done'%(counter, len(usernames), name))
	        
	        else:
	            counter+=1
	            print('%d/%d \t """%s""" is a private/verified account or has many contats'%(counter, len(usernames), name))
	    except:
	        counter+=1
	        print('%d/%d \t """%s""" This account does not exist anymore'%(counter, len(usernames), name))

	if save:
	    path = res_dir+username
	    os.mkdir(path)    
	    functions.write_json_lst(data, res_dir+username+'_complete.txt')
	    functions.write(usernames, res_dir+username+'_usernames.txt')
	    functions.write(ids, res_dir+username+'_ids.txt')
else:
	print('"""%s""" is a private/verified account or has many contats'%(username))


print("\nDONE")
