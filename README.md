# Two-approaches-to-digital-social-networks
Laitinen, Mikko, Masoud Fatemi & Jonas Lundberg. Size matters: Two approaches to digital social networks.


“Collecting_one_ego_net.py”**:
Gets a twitter username and extracts its friends’ list and the friends of friends list and saves the result in .txt and .json format. Using the extracted list you can create the friends/following ego network for the account of interest. 


“Extracting_tweets_ego_net.py”**:
Uses the result of Collecting_one_ego_net.py and retrieves tweets of the friends net up 3200 tweets per account. 


“english.py”, “lexico-grammar.py”, “spelling.py” and “lexis.py”:
Read all the retrieved tweets related to the entire network and extract the dependant variables. There is a binary variable inside the scripts as “save”, making it True will save the extracted variables as well. For the lexico-gramm, spelling, and lexis you could have your interested features. Just need to change the current verb, A/B sets and patterns respectively inside the codes and set them with your desired values.


“functions.py” and “info_diff_func.py”:
Are extra functions for ego-centric networks analysis. You will not need to use them directly, they will be used inside the other scripts.


“network_features.py”:
Extracts graph-based features from the ego network for the interested username/account. There are multiple functions and features (check the paper), you can extract them at the same time (takes time) or just extract the one that you are interested in (comment the other functions). 


“Visualizing_variables.py”:
Visualizes both the dependant variables and network-based features that have been calculated in the previous steps. It creates the heat-map and spider charts that have been included in the paper. Depend on what set of features you want to plot you can comment some part of the codes.


**use must have twitter credential key if you want to run the script.
