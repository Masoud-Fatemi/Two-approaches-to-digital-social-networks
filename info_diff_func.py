#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 18:41:05 2019
@author: masoud

extra functions for ego analysis
"""

import numpy as np
import networkx as nx
import pandas as pd
import random
import matplotlib.pyplot as plt
import seaborn as sns
import functions
from datetime import date
import calendar

def prepare_data(raw_data, base_ids, base_usernames):
    data = []
    ids = []
    usernames = []
    for item in raw_data:
        for key, value in item.items():
            
            usernames.append(key)
            new_key = base_ids[base_usernames.index(key)]
            ids.append(new_key)                
            data.append({new_key:{'friends':value['friends']}})
    return data, ids, usernames

def adjacency(ids, data):
    
    adj = np.zeros((len(ids), len(ids)))
    for item in data:
        for key, value in item.items():
            
            idx = ids.index(key)
            v = value['friends']
            for i in v:
                if str(i) in ids:
                    adj[idx][ids.index(str(i))] = 1 
    return adj

def simple_graph(adj):
    df = pd.DataFrame(adj)
    G = nx.DiGraph(df.values)
#    print(nx.info(G), "\n")
    return G

def links(adj):
    one_way = []
    two_way = []
    for i in range(len(adj)):
        for j in range(len(adj)):
            if adj[i][j] == 1.0 and adj[j][i] == 0:
                one_way.append((str(i),str(j)))
            elif adj[i][j] == 1.0 and adj[j][i] == 1.0:
                two_way.append((str(i),str(j)))
    return one_way, two_way

def edge_ratio(alfa, one, two, base):

    r = (alfa*(one/base)) + ((1-alfa)*(two/base))
    return round(r, 2)

def completeness(n, m):
    max_edges = n*(n-1)
    if max_edges == 0:
        completeness = 0
    else:
        completeness = m/(max_edges)
    return round(completeness, 4)

def plot_2D_graph_revised(dir_adj, usernames, friend=False,
                          circle=False, 
                          exclude_ego=False, 
                          with_labels=False, 
                          node_size=500, 
                          width=1, 
                          name_label=False,
                          ):
    
    one_way = []
    two_way = []
    for i in range(len(dir_adj)):
        for j in range(len(dir_adj)):
            if dir_adj[i][j] == 1.0 and dir_adj[j][i] == 0:
                one_way.append((str(i),str(j)))
            elif dir_adj[i][j] == 1.0 and dir_adj[j][i] == 1.0:
                two_way.append((str(i),str(j)))
    G = nx.DiGraph()         
    for i in one_way:
        G.add_edge(i[0],i[1], color='blue')

    for j in two_way:
        G.add_edge(j[0],j[1], color='black')
        G.add_edge(j[1],j[0], color='black')
        
    edges = G.edges()
    colors = [G[u][v]['color'] for u,v in edges]
        
    if circle:
        pos=nx.circular_layout(G, scale=1)
        pos['0'] = np.array([0, 0])
    else:
        pos=nx.spring_layout(G)
    
    if name_label:
        label_dict = {}
        for i in range(len(usernames)):
            label_dict[str(i)]=usernames[i]
    else:
        label_dict = {str(i):i for i in range(len(usernames))}
        
    node_color = len(dir_adj)*['red']
    if exclude_ego:
        node_color[list(pos.keys()).index('0')] = 'yellow'
        
    nx.draw(G,
            pos=pos,
            edges=edges,
            edge_color=colors,
            node_color=node_color,
            with_labels=with_labels,
            node_size=node_size,
            width=width,
            labels=label_dict)
   
    return True

def jaccard(data):
    
    similarity = np.zeros((len(data), len(data)))
    fr_s = []

    for i in range(len(data)-1):
        user1 = data[i]
        a = set(list(user1.values())[0]['friends'])
        for j in range(i+1, len(data)):
            user2 = data[j]
            b = set(list(user2.values())[0]['friends'])
            if len(b) != 0 and len(a) != 0:
                s = round((len(a.intersection(b)))/(len(a.union(b))), 4)
            else:
                s = 0
            similarity[i][j] = s
            fr_s.append(s)

    return similarity, fr_s

def jaccard_fri_in_net(data, ids):
    v = []
    similarity = np.zeros((len(data), len(data)))
    for i in range(len(data)-1):
        
        user1 = data[i]
        a = list(user1.values())[0]['friends']
        a = [i for i in a if str(i) in ids]
        a = set(a)
    
        for j in range(i+1, len(data)):
            
            user2 = data[j]
            b = list(user2.values())[0]['friends']
            b = [i for i in b if str(i) in ids]
            b = set(b)
            
            if len(b) != 0 and len(a) != 0:
                s = round((len(a.intersection(b)))/(len(a.union(b))), 3)
            else:
                s = 0
            similarity[i][j] = s
            v.append(s)
    
    return similarity, v

def jaccard_net_size(data, ids):
    
    v = []
    similarity = np.zeros((len(data), len(data)))
    for i in range(len(data)-1):
        
        user1 = data[i]
        a = list(user1.values())[0]['friends']
        a = [i for i in a if str(i) in ids]
        a = set(a)
    
        for j in range(i+1, len(data)):
            
            user2 = data[j]
            b = list(user2.values())[0]['friends']
            b = [i for i in b if str(i) in ids]
            b = set(b)
            
            if len(b) != 0 and len(a) != 0:
                s = round((len(a.intersection(b)))/(len(data)), 4)
            else:
                s = 0
            similarity[i][j] = s
            v.append(s)
    
    return similarity, v

def sampling_data(data, usernames, ids, samples=20):
    
    idx = [i for i in range(len(data))]
    idx = random.sample(idx, 20)
    if 0 not in idx:
        idx.append(0)
    idx.sort()
    usernames= [usernames[i] for i in idx]
    data = [data[i] for i in idx]
    ids = [ids[i] for i in idx]
    
    return data, usernames, ids

def heatmap(m, names):
    df = pd.DataFrame(m, index=names, columns=names)
    plt.figure(figsize = (10,7))
    sns.heatmap(df, annot=True, cmap="Reds")
    return True

def activity_stat(path, usernames, ids, adj):
    
    rt_c = np.zeros((len(ids), len(ids)))
    qt_c = np.zeros((len(ids), len(ids)))
    rep_c = np.zeros((len(ids), len(ids)))
    node_w = np.zeros((len(ids)))
    
    for name in usernames:
        tweets = functions.load_json_list(path+name+'.json')
        
        for item in tweets:
            
            if 'retweeted_status' in item.keys() and item['retweeted_status']['user']['id_str'] in ids:
                rt_c[usernames.index(name)][ids.index(item['retweeted_status']['user']['id_str'])]+=1
            
            #if its a quoted tweet from and account in the friend net then update qt_count value
            if item['is_quote_status']==True and 'quoted_status' in item.keys():
                if item['quoted_status']['user']['id_str'] in ids:
                    qt_c[usernames.index(name)][ids.index(item['quoted_status']['user']['id_str'])]+=1
            
            #if its a reply(mention) tweet to an account from the friend net then update rep_count value
            if item['in_reply_to_user_id'] != None and str(item['in_reply_to_user_id']) in ids:
                rep_c[usernames.index(name)][ids.index(str(item['in_reply_to_user_id']))]+=1
                
        if len(tweets)>0:
            item1=tweets[-1]
            item2=tweets[0]
            idx = usernames.index(name)
            node_w[idx] = nodes_stat(item1, item2, len(tweets))
        else: 
            node_w[idx] = 0
    
    np.fill_diagonal(rt_c, 0)
    np.fill_diagonal(qt_c, 0)
    np.fill_diagonal(rep_c, 0)
    
    return rt_c, qt_c, rep_c, node_w

def nodes_stat(item1, item2, l):
    
    abbr_to_num = {name: num for num, name in enumerate(calendar.month_abbr) if num}
    d0 = date(int(item1['created_at'].split()[-1]), abbr_to_num[item1['created_at'].split()[1]], int(item1['created_at'].split()[2]))
    d1 = date(int(item2['created_at'].split()[-1]), abbr_to_num[item2['created_at'].split()[1]], int(item2['created_at'].split()[2]))
    age=d1-d0
    n_w = round(age.days/l, 4)
    return n_w

def edge_weights(w, rt_c, qt_c, rep_c,adj,l):
    e = np.zeros((l, l))
    for i in range(len(e)):
        for j in range(len(e)):
            if adj[i][j] == 1:
                weight = 1 + (w[0]*rt_c[i][j]) + (w[1]*qt_c[i][j]) + (w[2]*rep_c[i][j])
                e[i][j] = round(weight,0)
    return e

def min_max_normalize(l):
    mi = np.min(l)
    ma = np.max(l)
    new = []
    for item in l:
        v = (item-mi)/(ma-mi)
        new.append(round(v, 2))
    return new

def read_multiple_net(accounts, adr):
    
    data, ids, usernames, color = [], [], [], []
    counter = 0
    for acc in accounts:
        path = adr+'/'+acc

        #read data for current user
        raw_data = functions.load_json_list(path+'/'+acc+'_complete.txt')
        base_usernames = functions.load(path+'/'+acc+'_usernames.txt')
        base_ids = functions.load(path+'/'+acc+'_ids.txt')
    
        #substitution usernames with user ids for current user
        temp_data, temp_ids, temp_usernames = prepare_data(raw_data, base_ids, base_usernames)
        data, ids, usernames, color = update_data(data, 
                                                  ids, 
                                                  usernames, 
                                                  temp_data, 
                                                  temp_ids, 
                                                  temp_usernames, 
                                                  color)
        counter+=1
        color = update_color(color, len(data), counter)
    return data, ids, usernames, color
    
def update_data(data, ids, usernames, temp_d, temp_i, temp_u, c):
    for i in temp_i:
        if i in ids:
#            c[ids.index(i)] = 0
            print("common user: ", temp_u[temp_i.index(i)])
        else:
            data.append(temp_d[temp_i.index(i)])
            ids.append(i)
            usernames.append(temp_u[temp_i.index(i)])

    return data, ids, usernames, c
    
def update_color(c, n, cnt):
    delta = n - len(c)
    for i in range(delta):
        c.append(cnt-1)
    return c
    
def disjointness(data, ids):
    
    new_data, new_ids = data[1:], ids[1:]
    new_adj = adjacency(new_ids, new_data)
    axis0 = np.sum(new_adj, axis=0)
    axis0 = list(axis0)
    axis1 = np.sum(new_adj, axis=1)
    axis1 = list(axis1)
    counter = 0
    for i in range(len(axis0)):
        if axis0[i] == 0.0 and axis1[i] == 0.0:
            counter += 1
    return counter/len(axis0)