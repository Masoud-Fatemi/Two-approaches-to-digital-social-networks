#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 13:35:52 2019
@author: masoud
"""

import functions
import random
import info_diff_func
import numpy as np
import networkx as nx
import operator

seed = 2
np.random.seed(seed)
random.seed(seed); del seed

user='INTERESTED ACCOUNT'

alfa = 0.4
extracting_weights = False
plot = True
disjoint = False
bc_analysis = False
cc_analysis = False
jsc = False
sdi = False
entropy = False
w = [0.2,0.5,0.3] #ret, qt, rep

path = 'EGOS DIRECTORY'+user
raw_data = functions.load_json_list(path+'/'+user+'_complete.txt')
base_usernames = functions.load(path+'/'+user+'_usernames.txt')
base_ids = functions.load(path+'/'+user+'_ids.txt')

data, ids, usernames = info_diff_func.prepare_data(raw_data, base_ids, base_usernames)

print("\n===========",user,"===========\n")

#creating adjacency matrix
adj = info_diff_func.adjacency(ids, data)

#a simple directed graph using networkx
G = info_diff_func.simple_graph(adj)                   

#extracting links
one_way, two_way = info_diff_func.links(adj)

#extracting the ratio of 1-way edges to 2-way edges
link_ratio = info_diff_func.edge_ratio(alfa, len(one_way), len(two_way), len(G.edges))
print ("edges ratio:", round(link_ratio, 2))

#how network is close to be a complete graph
completeness = info_diff_func.completeness(len(G.nodes), len(G.edges))
print("completeness:", str(completeness*100)+"%")

#calculating loss rate for the friend network
loss_ratio = (1 - (len(ids)/len(base_ids)))*100
print("loss ratio:", str(round(loss_ratio, 0))+"%")

"""calculating disjoint nodes via removing ego node"""
if disjoint:
    new_data, new_ids, new_usernames = data[1:], ids[1:], usernames[1:]
    new_adj = info_diff_func.adjacency(new_ids, new_data)
    axis0 = np.sum(new_adj, axis=0)
    axis0 = list(axis0)
    axis1 = np.sum(new_adj, axis=1)
    axis1 = list(axis1)
    counter = 0
    for i in range(len(axis0)):
        if axis0[i] == 0.0 and axis1[i] == 0.0:
            counter+=1
    print("Disjointness after removing ego node:", round(counter/(len(G.nodes)), 3)*100,"%")

#extracting features based on the activity
if extracting_weights:
    path = path+'/tweets/'
    rt_c, qt_c, rep_c, node_w = info_diff_func.activity_stat(path, usernames, ids, adj)
    edge_w = info_diff_func.edge_weights(w,rt_c, qt_c, rep_c,adj,len(ids))
    print("\nmean node weights:", round(np.mean(sum(node_w)), 2))
    print("mean edge weights:", round(np.mean(sum(edge_w)), 2))

"""plotting the network"""
if plot:
    info_diff_func.plot_2D_graph_revised(adj,usernames,
                                circle=False,
                                width=2,
                                node_size=1500,
                                with_labels=True,
                                exclude_ego=True,
                                name_label=False)

"""betweenness centrality"""
if bc_analysis:
    bc = dict(nx.betweenness_centrality(G))
    bc=sorted(bc.items(), key=operator.itemgetter(1), reverse=True)
    print("\n==========BC analysis==========")
    print("BC domain:", round(bc[0][1],4) - round(bc[-1][1],4))
    bc = [i[1] for i in bc]
    print("BC variance:", round(np.var(bc),4))
    print("BC mean:", round(np.mean(bc),4))
    
"""closeness centrality"""
if cc_analysis:
    
    cc_incoming = dict(nx.closeness_centrality(G))
    cc_incoming = sorted(cc_incoming.items(), key=operator.itemgetter(1), reverse=True)
    print("\n==========CC analysis==========")
    cc_incoming = [i[1] for i in cc_incoming]
    cc_incoming_mean = round(np.mean(cc_incoming),2)
    print("CC incoming mean:", cc_incoming_mean)  
    
    R = G.reverse()
    cc_outward = dict(nx.closeness_centrality(R))
    cc_outward=sorted(cc_outward.items(), key=operator.itemgetter(1), reverse=True)
    cc_outward = [i[1] for i in cc_outward]
    cc_outward_mean = round(np.mean(cc_outward),2)
    print("CC outward mean:", cc_outward_mean) 
    print("CC difference bet outward and incoming:", cc_outward_mean - cc_incoming_mean)
"""Jaccard Similarity Index"""
if jsc:
    
    print("\n==========JSC analysis==========")
    
#    data, usernames, ids = info_diff_func.sampling_data(data, usernames, ids, 20)
    
    sim, values = info_diff_func.jaccard(data)
    print("mean Similarity:", round(np.mean(values),4))

    sim, values = info_diff_func.jaccard_net_size(data, ids)
    print("mean Similarity (net size):",round(np.mean(values), 4))
    
    sim, values = info_diff_func.jaccard_fri_in_net(data, ids)
    print("mean Similarity (friends in the net):",round(np.mean(values), 4))
    
        
#    info_diff_func.heatmap(sim, usernames)