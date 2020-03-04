#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 15:25:13 2019
@author: masoud
"""
import matplotlib.pyplot as plt
import pandas as pd
from math import pi
import seaborn as sns
import info_diff_func
import scipy as sp


"""spider chart or heatmap for dependent variables """    
hashtags = [0.00012, 0.00003, 0.00003, 0.00012, 0.00010, 0.00003, 0.00001, 0.00009, 0.00009, 0.00011, 0.00002]
spelling = [0.0386, 0.0259, 0.0293, 0.0094, 0.0358, 0.0323, 0.0579, 0.0189, 0.0261,  0.0380,  0.0629]
lexico = [0.0063, 0.0084, 0.0066, 0.0031, 0.0077, 0.0056, 0.0089, 0.0060, 0.0045, 0.0061,  0.0107]
english = [0.63220, 0.79534, 0.61039, 0.40910, 0.81195, 0.45237, 0.85387, 0.60193, 0.62170, 0.68688, 0.81261]
accounts = ["YOUR ACCOUNTS"]
#
hashtags = info_diff_func.min_max_normalize(hashtags)
spelling = info_diff_func.min_max_normalize(spelling)
lexico = info_diff_func.min_max_normalize(lexico)
english = info_diff_func.min_max_normalize(english)

hashtags = [i*90 for i in hashtags]
spelling = [i*90 for i in spelling]
lexico = [i*90 for i in lexico]
english = [i*90 for i in english]

hashtags = [i+10 for i in hashtags]
spelling = [i+10 for i in spelling]
lexico = [i+10 for i in lexico]
english = [i+10 for i in english]

df = pd.DataFrame({'accounts':accounts, 'hashtags':hashtags, 'spelling':spelling, 'lexico':lexico, 'english':english})

# number of variables 
categories=list(df)[1:]
N = len(categories)

# What will be the angle of each axis in the plot? (we divide the plot / number of variable)
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]

# Initialise the spider plot
ax = plt.subplot(111, polar=True)

# If you want the first axis to be on top:
ax.set_theta_offset(pi / 2)
ax.set_theta_direction(-1)

# Draw one axe per variable + add labels labels yet
plt.xticks(angles[:-1], categories)

# Draw ylabels
ax.set_rlabel_position(0)
plt.yticks([25,50,75], ["25","50","75"], color="grey", size=7)
plt.ylim(0,100)

plt.yticks([-1,0,1], ["-1","0","1"], color="grey", size=7)
plt.ylim(-2,2)

for i in range(len(accounts)):
    values=df.loc[i].drop('accounts').values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=2, linestyle='solid', label=accounts[i])
    ax.fill(angles, values, 'b', alpha=0.1)

# Add legend
plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

hashtags = sp.stats.zscore(hashtags)
spelling = sp.stats.zscore(spelling)
lexico = sp.stats.zscore(lexico)

df = pd.DataFrame({'hashtags':hashtags, 'spelling':spelling, 'lexico':lexico}, index=accounts)
plt.figure(figsize = (10,7))
#sns.heatmap(df, annot=True, cmap="Reds")




"""heatmap for analyzing net types"""
bc_spr = [0.4310, 0.3860, 0.5908, 0.6099, 0.7423, 0.7674, 0.5444, 0.5395, 0.7773, 0.5376]
bc_mean = [0.0063, 0.0063, 0.0044, 0.0059, 0.0087, 0.0074, 0.0047, 0.0037, 0.0044, 0.0035]
jsc_mean = [0.0032,0.0067,0.0247,0.0091,0.0097,0.0180,0.0093,0.0085, 0.0080, 0.0221]
edge_w = [7.98, 9.23, 48.55, 10.01, 7.42, 13.9, 19.03, 19.13, 9.45, 39.55]
disjointness = [17.7, 9.1, 1, 16.1, 17.3, 16.8, 5.4, 7.4, 28.8, 2]
cc_difference = [0.04, 0.02, 0.0, 0.02, 0.01, 0.01, 0.02, 0.02, 0.01, 0.0]
#
bc_spr = info_diff_func.min_max_normalize(bc_spr)
bc_mean = info_diff_func.min_max_normalize(bc_mean)
jsc_mean = info_diff_func.min_max_normalize(jsc_mean)
edge_w = info_diff_func.min_max_normalize(edge_w)
disjointness = info_diff_func.min_max_normalize(disjointness)
cc_difference = info_diff_func.min_max_normalize(cc_difference)
#
bc_mean = [round(1-i,2) for i in bc_mean]
bc_spr = [round(1-i,2) for i in bc_spr]
disjointness = [round(1-i,2) for i in disjointness]
cc_difference = [round(1-i,2)for i in cc_difference]

accounts = ['account_01', 'account_02', 'account_03', 'account_04', 'account_05','account_06','account_07','account_08', 'account_09', 'account_10']
accounts = ['W1', 'S6', 'S7', 'W2', 'W3','W4','S8','S9', 'W5', 'S10']

df = pd.DataFrame({'BC mean   ':bc_mean, 'BC spread':bc_spr,  'JCS':jsc_mean, 'closeness\ncentrality':cc_difference,
                    'disjointness':disjointness, 'edge\nweight':edge_w, },
                     index=accounts)

    
plt.rcParams.update({'font.size': 16, 'font.sans-serif':'Arial'})
plt.rcParams.update({'axes.labelweight': 'bold',})
plt.rcParams.update({'axes.labelsize': 'large',})
plt.rcParams.update({'xtick.labelsize': 'large'})
plt.rcParams.update({'ytick.labelsize': 'large'})

plt.figure(figsize = (20,15))
sns.heatmap(df, annot=True, cmap="Reds")

categories=list(df)
N = len(categories)

ax = plt.subplot(111, polar=True)

# If you want the first axis to be on top:
ax.set_theta_offset(pi / 2)
ax.set_theta_direction(-1)

# Draw one axe per variable + add labels labels yet
angles = [n / float(N) * 2 * pi for n in range(N)]
plt.xticks(angles, categories)

# Draw ylabels
ax.set_rlabel_position(0)
plt.yticks([.25,.50,.75], ["0.25","0.50","0.75"], color="grey", size=7)
plt.ylim(0,1)

weak_tie = [0,3,4,5,8]
strong_tie = [1,2,6,7,9]

angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]

for i in weak_tie:
    values=df.iloc[i].values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=2, linestyle='solid', label=accounts[i])
    ax.fill(angles, values, 'b', alpha=0.1)
    
plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    
del pi,