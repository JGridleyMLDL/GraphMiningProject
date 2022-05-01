# Created by Jared Gridley on 03/22/2022
#
# utils.py
#
#

import pandas as pd
import networkx as nx
import matplotlib as mpl
import matplotlib.pyplot as plt


def extract_Addr(ad):
    """Extracts Wallet Address from Amberdata return field

    Args:
        ad (list(dict)): Address data (include hex string and sometimes name)

    Returns:
        string: human-readable string
    """

    if "nameNormalized" in ad[0].keys():
        return ad[0]["nameNormalized"]

    return ad[0]["address"]


def gwei_usd(d):
    """Converts GWEI amounts to USD based on current (03/22/2022)
    conversion rate. 
        THIS IS AN ESTIMATION TO MAKE THE GRAPH MORE READABLE

    Args:
        d (string): GWEI Amount (from value field in AmberData return)

    Returns:
        float: Amount in USD
    """
    return 0.00000000000000235 * float(d)


def draw_transaction_graph_heatmap(G, addr, labels=True):
    """Used Matplotlib to draw a heatmap graph showing
    the number of transactions between addresses (nodes)

    Args:
        G (networkx.classes.digraph.DiGraph): Directed Graph of Transactions
        addr (string): Original Address
    """
    pos = nx.spring_layout(G)

    M = G.number_of_edges()
    edge_colors = range(2, M + 2)
    edge_alphas = [(5 + i) / (M + 4) for i in range(M)]
    cmap = plt.cm.YlOrRd

    nodes = nx.draw_networkx_nodes(
        G, pos, node_size=20, node_color="indigo")
    edges = nx.draw_networkx_edges(
        G,
        pos,
        node_size=5,
        arrowstyle="->",
        arrowsize=20,
        edge_color=edge_colors,
        edge_cmap=cmap,
        width=2,
    )

    if labels:
        nx.draw_networkx_labels(
            G,
            pos,
            font_size=8,
            horizontalalignment='right',
            verticalalignment='top',
            clip_on=False
        )

    # set alpha value for each edge
    for i in range(M):
        edges[i].set_alpha(edge_alphas[i])

    plt.title("Txs:  {0}".format(addr))
    pc = mpl.collections.PatchCollection(edges, cmap=cmap)
    pc.set_array(edge_colors)
    cbar = plt.colorbar(pc)
    cbar.set_label('# of transactions')

    ax = plt.gca()
    ax.set_axis_off()
    plt.show()


def normalize_df(df):
    df['from'] = df['from'].apply(extract_Addr)
    df['to'] = df['to'].apply(extract_Addr)
    return df


def create_transaction_graph(df):
    """Parses the dataframe and forms a networkx graph
    inluding normalizing addresses and transaction amounts

    Args:
        df (pandas dataframe): dataframe of transactions

    Returns:
        networkx.DiGraph: Graph representation of transactions
    """
    pd.options.mode.chained_assignment = None
    graph_df = df[['blockNumber', 'from', 'to', 'value']]

    # Standardizing Data
    graph_df['from'] = graph_df['from'].apply(extract_Addr)
    graph_df['to'] = graph_df['to'].apply(extract_Addr)
    graph_df['value'] = graph_df['value'].apply(gwei_usd)

    G = nx.from_pandas_edgelist(graph_df,
                                source='from',
                                target='to',
                                edge_attr='value',
                                create_using=nx.DiGraph())

    print("Update:\t {0} transactions found between {1} addresses".format(
        graph_df.shape[0], G.number_of_nodes()))

    return G
