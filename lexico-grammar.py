#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 15:32:15 2019
@author: masoud
"""

import functions
import os
import sys
from nltk import WhitespaceTokenizer
from nltk import ngrams
from nltk import pos_tag
import re

username='INTERESTED ACCOUNT'
save = False

input_dir = 'TWEETS DIRECTORY'
output_dir = 'RESULT DIRECTORY'


verb = ['need to', 'needed to', 'needs to']

result = {}
res = ['username \t tweet_id \t tweet_text \t date_and_time']
directory = os.fsencode(input_dir)
num_of_files = len([name for name in os.listdir(directory)])
counter = 0
tweets_counter = 0
instance_counter = 0

for file in os.listdir(directory):
    
    file_name = os.fsdecode(file)
    path = input_dir + file_name
    data = functions.load_json_list(path)
    tweets_counter += len(data)
    counter+=1

    id_date = []
    for item in data:
        
        for i in verb:
            if re.search(i, item['full_text'].lower()):
                
                text = functions.clean_text(item['full_text'])
                text = functions.give_emoji_free_text(text)
                text = functions.additional_remove(text)
                text = text.lower()
        
                tokens = WhitespaceTokenizer().tokenize(text)
                tokens = [x.lower() for x in tokens]
                tags = pos_tag(tokens)

                grams = []
                for j in ngrams(tokens, 2):
                    grams.append(' '.join([x for x in j]))
                    
                for gram in grams:
                    if gram == i:
                        idx = grams.index(gram)
                        if idx<len(tags)-2:
                            if tags[idx+2][1] in ['VB', 'VBP']:
                                id_date.append((item['id_str'], item['created_at']))
                                
                                res.append(item['user']['screen_name']+'\t'+item['id_str']+'\t'+text+'\t'+item['created_at'])
    instance_counter += len(id_date)
    if len(id_date)>0:
        file_name = file_name.split('.',-1)[0]
        result[file_name] = id_date
    sys.stdout.write('\r%d/%d'%(counter,num_of_files))

print("\nnumber of tweets;", tweets_counter)
print("found instaces: ", instance_counter)
print("final value:", round(instance_counter/tweets_counter,4))    

if save:
    functions.write_json(result, output_dir+'lexico-grammar('+verb[0]+').json')
    functions.write(res, output_dir+'lexico-grammar('+verb[0]+').txt')