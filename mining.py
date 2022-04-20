import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from tqdm import tqdm
import collections
import utils
import make_query
import queries
import control
import visualizations


#
# This file contains Graph mining metrics for analyzing transactions
# Graphs. Many algorithms are taken or modified from Graph Mining
# class examples: https://www.cs.rpi.edu/~slotag/classes/SP22m/index.html
#


def avg_shortest_path(G):
    avg_shortest_paths = 0.0

    tot_len = 0
    num_nodes = 0

    for n in G.nodes():
        d = nx.shortest_path_length(G, n)
        tot_len += sum(list(d.values()))
        num_nodes += len(d)

    avg_shortest_paths = tot_len/num_nodes

    print("Average shortest path length: {0:.2f}".format(avg_shortest_paths))
    return avg_shortest_paths


def connected_components(G):
    """Returns connected components of G

    Args:
        G (nx.Graph or nx.MultiGraph): Undirected Graph

    Returns:
        list: Connected Components
    """
    isc = nx.is_connected(G)
    ncc = nx.number_connected_components(G)

    print("G is Connected:", isc)
    print("{0} Connected Components in G".format(ncc))

    C = nx.connected_components(G)

    CC_sizes = []
    for c in C:
        CC_sizes.append(len(c))

    print("Connected Component Sizes:", CC_sizes)
    return C


def strong_weak_connected_components(G):
    """Get Strongly and Weakly Connected Components and 
    prints some information on the Connected Component Sizes

    Args:
        G (DiGraph or MultiDiGraph): Directed Graph 

    Returns:
        tuple: (Strongly Connected Components, Weakly Connected Components)
    """
    sccs = nx.strongly_connected_components(G)

    scc_sizes = []
    for s in sccs:
        scc_sizes.append(len(s))
    scc_counts = collections.Counter(scc_sizes)

    print("Strongly Connected Component Sizes:")
    for i in scc_counts.keys():
        print("\tFound {0} SCCs with size {1}.".format(scc_counts[i], i))

    wcc = nx.weakly_connected_components(G)

    wcc_sizes = []
    for s in wcc:
        wcc_sizes.append(len(s))
    wcc_counts = collections.Counter(wcc_sizes)

    print("Weakly Connected Component Sizes:")

    for i in wcc_counts.keys():
        print("\tFound {0} WCCs with size {1}.".format(wcc_counts[i], i))

    return sccs, wcc


def degree_dist(G):
    degrees = {}

    in_degrees = {}
    for v in G.nodes():
        d = G.degree(v)
        if d not in degrees:
            degrees[d] = 1
        else:
            degrees[d] += 1

    sorted_degrees = sorted(degrees.items())
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot([k for (k, v) in sorted_degrees],
            [v for (k, v) in sorted_degrees])
    ax.set_xlabel("Degrees of Each Vertex")
    ax.set_ylabel("Num nodes with Degree D")
    ax.set_title("Degree Distribution of Graph")
    ax.set_xscale('log')
    ax.set_yscale('log')
    plt.show()


def power_law_coeff(G):
    pl_coefficient = 0.0

    tot_deg = 0
    num_nodes = 0
    for v in G.nodes():
        num_nodes += 1

        tot_deg += np.log(G.degree(v))

    pl_coefficient = 1 + (num_nodes / tot_deg)

    print("Power-law coefficient:", pl_coefficient)
    return pl_coefficient


def hub_ratio_estimation(G):
    hub_ratio = 0.0

    num_nodes = G.number_of_nodes()
    thr = np.log(num_nodes)

    t = 0
    for v in G.nodes():

        deg = G.degree(v)
        if deg > thr:
            t += 1

    hub_ratio = t / num_nodes

    print("{0} hubs identified from {1} nodes:".format(t, num_nodes))
    print("Hub Ratio Degree Threshold: {0:.2f}".format(thr))
    print("Ratio of hubs: {0:.8f}".format(hub_ratio))


def centrality_detection(G):
    degree_cent = nx.degree_centrality(G)

    degree_cent_sorted = sorted(degree_cent.items(),
                                key=lambda item: item[1], reverse=True)

    close_cent = nx.closeness_centrality(G)

    close_cent_sorted = sorted(close_cent.items(),
                               key=lambda item: item[1], reverse=True)

    print("Most Central Addresses (Degree): ",
          degree_cent_sorted[0:5], end="\n\n")
    print("Most Central Addresses (Closeness): ",
          close_cent_sorted[0:5], end="\n\n")
    print("Least Central Tokens (Degree): ",
          degree_cent_sorted[-5:], end="\n\n")
    print("Least Central Tokens (Closeness): ",
          close_cent_sorted[-5:], end="\n\n")

    return degree_cent_sorted, close_cent_sorted


# Want to do community detection/clustering as well.
