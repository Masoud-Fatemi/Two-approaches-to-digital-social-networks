#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 22:31:27 2019
@author: masoud
"""

import functions
import os
import sys
from nltk import WhitespaceTokenizer
from nltk import ngrams

username='INTERESTED ACCOUNT'
save = False

input_dir = 'TWEETS DIRECTORY'
output_dir = 'RESULT DIRECTORY'

A = ['is not', 'are not', 'was not', 'were not',
     'have not','has not', 'had not', 'can not','cannot', 'could not', 'i have', 'i am', 'i would', 'i had']

B = ['isn’t', 'aren’t', 'wasn’t', 'weren’t', 'isnt', 'arent', 'wasnt', 'werent',
     'haven’t','hasn’t', 'hadn’t', 'hasnt', 'havent', 'hadnt',
     'can’t', 'couldn’t', 'cant', 'couldnt', 'i’ve', 'i’m', 'i’d']

result = {}
res = ['username \t tweet_id \t tweet_text \t date_and_time']
directory = os.fsencode(input_dir)
num_of_files = len([name for name in os.listdir(directory)])
counter = 0
tweets_counter = 0
a_values_counter = 0
b_values_counter = 0

for file in os.listdir(directory):
    
    file_name = os.fsdecode(file)
    path = input_dir + file_name
    data = functions.load_json_list(path)
    tweets_counter += len(data)
    counter+=1
    temp = {}
    a_values = []
    b_values = []
    
    for item in data:
        
        text = functions.clean_text(item['full_text'])
        text = functions.give_emoji_free_text(text)
        text = functions.additional_remove(text)
        tokens = WhitespaceTokenizer().tokenize(text)
        tokens = [x.lower() for x in tokens]

        for t in tokens:
            if t in B:
                b_values.append((item['id_str'], item['created_at']))
                res.append(item['user']['screen_name']+'\t'+item['id_str']+'\t'+text+'\t'+item['created_at'])
    
        for i in ngrams(tokens, 2):
            if ' '.join([j for j in i]) in A:
                a_values.append((item['id'], item['created_at']))
                res.append(item['user']['screen_name']+'\t'+item['id_str']+'\t'+text+'\t'+item['created_at'])
    
    a_values_counter+=len(a_values)
    b_values_counter+=len(b_values)
    
    if len(b_values)>0 or len(a_values)>0:
        temp['B_values'] = b_values
        temp['A_values'] = a_values
        file_name = file_name.split('.',-1)[0]
        result[file_name] = temp
    sys.stdout.write('\r%d/%d'%(counter,num_of_files))

print("\nnumber of tweets;", tweets_counter)

print("\nnumber of A values: ", a_values_counter)
print("number of B values: ", b_values_counter)
print("total values: ", a_values_counter+b_values_counter)

print("\nfinal A value:", round(a_values_counter/tweets_counter,4))
print("final B value:", round(b_values_counter/tweets_counter,4))
print("final total value:", round((a_values_counter+b_values_counter)/tweets_counter,4))

if save:
    functions.write_json(result, output_dir+'spelling.json')
    functions.write(res, output_dir+'spelling.txt')