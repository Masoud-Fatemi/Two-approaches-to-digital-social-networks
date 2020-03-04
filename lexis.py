#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 20:23:47 2019
@author: masoud
this code takes hashtag(s) as input and extracts tweet's data, tweet's and account(s)
that used that hastag(s) in their tweets in an ego net
"""

import functions
import os
import sys
import re


username='INTERESTED ACCOUNT'
save = False

input_dir = 'TWEETS DIRECTORY'
output_dir = 'RESULT DIRECTORY'

pattern = ['me_too','metoo']

result = {}
res = ['username \t tweet_id \t tweet_text \t date_and_time']
directory = os.fsencode(input_dir)
num_of_files = len([name for name in os.listdir(directory)])
counter = 0
hashtag_counter = 0
pattern = [i.lower() for i in pattern]
tweets_counter = 0

for file in os.listdir(directory):
    
    file_name = os.fsdecode(file)
    path = input_dir + file_name
    data = functions.load_json_list(path)
    tweets_counter += len(data)
    counter+=1
    
    t = []
    for item in data:
        if len(item['entities']['hashtags']) !=0: 
            for h in item['entities']['hashtags']:
                if h['text'].lower() in pattern:
                    t.append((item['id_str'], item['created_at'], h['text'].lower()))
                    hashtag_counter+=1
                    
                    text = item['full_text']
                    text = re.sub(r"http\S+", " ",text)
                    text = re.sub(r"\s+", " ", text)
                    res.append(item['user']['screen_name']+'\t'+item['id_str']+'\t'+text+'\t'+item['created_at'])
    
    if len(t)>0:
    
        file_name = file_name.split('.',-1)[0]
        result[file_name] = t
    sys.stdout.write('\r%d/%d'%(counter,num_of_files))

print("\nnumber of tweets;", tweets_counter)
print("found hashtags: ", hashtag_counter)
print("final value:", round(hashtag_counter/tweets_counter,5))

if save:
    functions.write_json(result, output_dir+'lexis('+pattern[0]+').json')
    functions.write(res, output_dir+'lexis('+pattern[0]+').txt')
    