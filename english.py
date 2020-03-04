#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 21:59:27 2019

@author: masoud
this code reads tweets for an ego net and extracts the share of english tweets.
"""

import functions
import os
import sys

username='INTERESTED ACCOUNT'
save = False

input_dir = 'TWEETS DIRECTORY'
output_dir = 'RESULT DIRECTORY'

directory = os.fsencode(input_dir)
num_of_files = len([name for name in os.listdir(directory)])

counter = 0
english_counter = 0
tweet_counter = 0

for file in os.listdir(directory):
    
    file_name = os.fsdecode(file)
    path = input_dir + file_name
    data = functions.load_json_list(path)
    tweet_counter += len(data)
    counter+=1
    
    for item in data:
        if item['lang'] == 'en':
            english_counter += 1

    sys.stdout.write('\r%d/%d'%(counter,num_of_files))
print("\n=========",username,"=========")
print("\nnumber of tweets;", tweet_counter)
print("found hashtags: ", english_counter)
print("final value:", round(english_counter/tweet_counter,5))