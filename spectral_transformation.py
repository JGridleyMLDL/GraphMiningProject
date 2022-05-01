# %%
import pandas as pd
import networkx as nx
from networkx.algorithms import bipartite
import random

import matplotlib as mlp
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
from sklearn import metrics
from scipy.optimize import curve_fit

import control
import make_query
import mining
import queries
import utils
import visualizations


# %% [markdown]
# ### Importing Temporal User Data from:
# - Uniswap
# - Compound
# - Decentraland
# - AAVE
# - Balancer
# - 1INCH
#
# The timeframe is from 1638334800 to 1648785600

# %%
# Open all the data

# Aggregate and add defi label

# bipatite matching like with amazon

# %%
aave = pd.read_csv("user_prediction_data/aave_data.csv")
axie = pd.read_csv("user_prediction_data/axie_data.csv")
balancer = pd.read_csv("user_prediction_data/balancer_data.csv")
compound = pd.read_csv("user_prediction_data/compound_data.csv")
decentraland = pd.read_csv("user_prediction_data/decentraland_data.csv")
oneInch = pd.read_csv("user_prediction_data/one_inch_data.csv")
uniswap = pd.read_csv("user_prediction_data/uniswap_data.csv")


# %%
def extract_users(df, col_name1, col_name2="", time_col="timestamp"):
    users = df[[col_name1, time_col]]
    users.columns = ["address", "time"]

    if col_name2 != "":
        more_users = df[[col_name2, time_col]]
        more_users.columns = ["address", "time"]
        users = pd.concat([users, more_users], axis=0)

    users.drop_duplicates()
    print(users.columns)

    return users


# %%
aave_users = extract_users(aave, "user.id")
aave_users["DeFi_APP"] = "Aave"
axie_users = extract_users(axie, "from.id", "to.id")
axie_users["DeFi_APP"] = "Axie"
balancer_users = extract_users(balancer, "userAddress.id")
balancer_users["DeFi_APP"] = "Balancer"
compound_users = extract_users(compound, "to", "from", "blockTime")
compound_users["DeFi_APP"] = "Compound"
decentraland_users = extract_users(decentraland, "buyer", "seller")
decentraland_users["DeFi_APP"] = "Decentraland"
one_inch_users = extract_users(oneInch, "from.id", "to.id")
one_inch_users["DeFi_APP"] = "1Inch"
uniswap_users = extract_users(uniswap, "sender", "to")
uniswap_users["DeFi_APP"] = "UniswapV2"


# %%
dfs = [aave_users, axie_users, balancer_users, compound_users,
       decentraland_users, one_inch_users, uniswap_users]

user_data = pd.concat(dfs)

# user_data.drop_duplicates(subset=user_data.columns.difference(['time']))


# %%
sorted_user_data = user_data.sort_values(by=["time"])
print(sorted_user_data.shape)

train_data = sorted_user_data.head(int(len(sorted_user_data)*(0.8)))
print(train_data.shape)


# %%
# this is generating a bipartite graph that is will have the the defi apps as one row and the addresses as another


def generate_bipartite_graph(df, source, target, edge):
    top = set(df[source])
    bot = set(df[target])

    G_nums = nx.from_pandas_edgelist(
        df, source, target, edge)
    edges = G_nums.edges(data=True)

    G_bi = nx.Graph()
    G_bi.add_nodes_from(top, bipartite=0)
    G_bi.add_nodes_from(bot, bipartite=1)
    G_bi.add_edges_from(edges)
    print(G_bi)

    return G_bi


# %%
# Dataframe to get counts for the number of times a user used a platform
df_count = sorted_user_data.groupby(
    ["address", "DeFi_APP"], as_index=False).size()


# testing on a random subset for visualization
df_count_small = df_count.sample(frac=0.2)
print(df_count_small.shape)

# generating the bipartite graph
G_bi = generate_bipartite_graph(df_count, "DeFi_APP", "address", "size")


# %%
# nx.draw(G_bi)
nx.is_connected(G_bi)

# %%
# get layout
print("Getting Layout")
top = nx.bipartite.sets(G_bi)[0]
pos = nx.bipartite_layout(G_bi, top)

print("Getting adjacency matrix")
# get adjacency matrix
A = nx.adjacency_matrix(G_bi)
A = A.toarray()

print(A)


# %%
# Remove 25% of the edges
proportion_edges = 0.25
# this is our test set
edge_subset = random.sample(G_bi.edges(), int(
    proportion_edges * G_bi.number_of_edges()))

# Create a copy of the graph and remove the edges
B_train = G_bi.copy()
B_train.remove_edges_from(edge_subset)
print("train:", B_train)

B_test = nx.Graph()
B_test.add_edges_from(edge_subset)
print("train:", B_test)


# %%
def MAP(G_test, G_pred, thres=0):
    # calculate avePrecision for each node and its neighbors
    avePs = []

    # loop through every node
    for node in tqdm(G_test.nodes()):
        # get predicted edges sorted in ranking order
        rankedPredWeights = sorted(
            G_pred[node].items(), key=lambda x: -x[1]['weight'])
        # only include edges that exist i.e. predicted rank / weight > threshold
        rankedPred = filter(
            lambda x: x[1]['weight'] > thres, rankedPredWeights)
        # get the rank
        pred = [x[0] for x in rankedPred]
        # calculate rel (existence of predicted edge in the groundtruth/actual set of edges)
        # get groundtruth neighbors
        gt = set(G_test[node])
        rel = np.array([x in gt for x in pred])
        # calculate P accumulative average of precision
        predLength = len(pred)
        P = np.array([
            sum(rel[:i+1])/len(rel[:i+1]) for i in range(predLength)
        ])
        # calculate aveP
        aveP = (rel @ P)/len(gt)
        # keep track of results
        avePs.append(aveP)
    MAPvalue = sum(avePs) / len(avePs)
    print("MAP: {}".format(MAPvalue))
    return MAPvalue


def ROC_PRC(pred, G):
    # prediction score
    y_score = [p[2] for p in pred]
    # groundtruth label
    y_true = [G.has_edge(p[0], p[1]) for p in pred]
    fig, (ax1, ax2) = plt.subplots(1, 2)
    # precision-recall curve
    fpr, tpr, thresholds = metrics.precision_recall_curve(y_true,  y_score)
    ax1.plot(fpr, tpr)
    ax1.set_title("Precision-Recall Curve")
    # receiver-operating characteristic curve
    fpr, tpr, thresholds = metrics.roc_curve(y_true, y_score)
    ax2.plot(fpr, tpr)
    ax2.set_title("ROC Curve, AUC = {:.2f}".format(
        metrics.roc_auc_score(y_true, y_score)))

    plt.show()


# %%
for algo in [
    nx.resource_allocation_index,
    nx.jaccard_coefficient,
    nx.adamic_adar_index
]:
    print(algo)
    pred = list(algo(B_train))
    # create graph
    G_pred = nx.Graph()
    G_pred.add_weighted_edges_from(pred)
    # visualise adjacency matrix
    Apred = nx.adjacency_matrix(G_pred)
    Apred = Apred.toarray()
    #plt.imshow(Apred, cmap='Greys')
    # plt.show()
    # evaluation
    print("Visualizations for", algo)
    ROC_PRC(pred, G_bi)
    MAP(B_test, G_pred)


# %% [markdown]
# We see that these methods will only predict existing edges between the same sets. This is because two vertices from different sets will never share common neighbors, resulting in a 0 MAP score.

# %%
A_train = nx.adjacency_matrix(B_train)
A_train = A_train.toarray()
A_train.shape


# %%
# eigenvalue decomposition
V_train, U_train = np.linalg.eig(A_train)
print("Found Eigenvalue Decomposition!")
# U.T * Atest * U
target_V = U_train.T @ A @ U_train
print("Found Target!")
# take only the diagonals
target_V = np.diag(target_V)


# %%


# %%


# %%


# %%


# %%
G = nx.from_pandas_edgelist(
    sorted_user_data, "address", "DeFi_APP", True)
print(G)


# %%


# %%
