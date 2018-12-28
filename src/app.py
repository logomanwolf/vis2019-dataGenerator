import networkx as nx
from networkx.readwrite import json_graph
import math
import json
import random


def clique(count, begin_id):
    G = nx.Graph()
    for i in range(count):
        for j in range(count - i - 1):
            G.add_edge(begin_id + i, begin_id + count - 1 - j)
    labels = 'clique'
    nx.set_node_attributes(G, labels, 'labels')
    return G

def bipartite(count, begin_id):
    G = nx.Graph()
    left_count = math.floor(count / 2)
    right_count = count - left_count
    for i in range(left_count):
        for j in range(right_count):
            G.add_edge(i + begin_id, begin_id + left_count + j)
    labels = 'bipartite'
    nx.set_node_attributes(G, labels, 'labels')
    return G

def star(count, begin_id):
    G = nx.Graph()
    for i in range(count - 1):
        G.add_edge(begin_id, begin_id + i + 1)
    labels = 'star'
    nx.set_node_attributes(G, labels, 'labels')
    return G

def king(count, begin_id):
    G = nx.Graph()
    length = math.floor(math.sqrt(count))
    for i in range(length):
        for j in range(length):
            if i > 0:
                G.add_edge(begin_id + i * length + j, begin_id + (i - 1) * length + j)
            if j > 0:
                G.add_edge(begin_id + i * length + j, begin_id + i * length + j - 1)

    for k in range(count - length * length):
        if k > 0:
            G.add_edge(length * length + begin_id + k, length * length + begin_id + k - 1)
        G.add_edge(length * length + begin_id + k, length * length + begin_id + k - length)
    labels = 'king'
    nx.set_node_attributes(G, labels, 'labels')
    return G

myPatterns = {
    'king': king,
    'star': star,
    'bipartite': bipartite,
    'clique': clique
}

def dynamic_graph(time_count, nodes_count, community_count_of_each_type, path_length = 3):
    graphs = []
    for i in range(time_count):
        graphs.append(static_graph(nodes_count, community_count_of_each_type, path_length))
    return graphs


def static_graph(nodes_count, community_count_of_each_type, path_length = 3):
    pattern_funcs = list(myPatterns.values())
    compound_G = nx.classic.cycle_graph(community_count_of_each_type * len(pattern_funcs)) # use cycle graph to connect components
    # compound_G = nx.expanders.chordal_cycle_graph(community_count_of_each_type * 4) # use chordal_cycle_graph to connect components
    path_nodes_count = len(compound_G.edges) * (path_length - 1)
    node_in_community_count = math.floor((nodes_count - path_nodes_count) / (community_count_of_each_type * len(pattern_funcs)))
    patterns = []
    begin_ids = []
    for i in range(community_count_of_each_type):
        j = 0
        random.shuffle(pattern_funcs)
        for pattern_func in pattern_funcs:
            begin_id = (i * len(list(myPatterns)) + j) * node_in_community_count
            begin_ids.append(begin_id)
            patterns.append(pattern_func(node_in_community_count, begin_id))
            j += 1
    G = nx.Graph()
    k = 0
    for pattern in patterns:
        group = k
        nx.set_node_attributes(pattern, group, 'group')
        k += 1
        G = nx.compose(G, pattern)
    for edge in compound_G.edges:
        count = len(G.nodes)
        G.add_edge(begin_ids[edge[0]], count)
        for i in range(path_length - 2):
            G.add_edge(count + i, count + i + 1)
        G.add_edge(count + path_length - 2, begin_ids[edge[1]])
    return G


if __name__ == "__main__":
    community_count = 20 # 社团总体数量，最好是4的倍数（因为图里面有四种pattern）
    nodes_count = 1000 # 每一帧的节点总体数量
    graphs = dynamic_graph(10, nodes_count, int(community_count / 4))
    # G = nx.classic.cycle_graph(40)
    # G = nx.expanders.chordal_cycle_graph(40)
    # G = nx.Graph()
    # G = nx.compose(G, clique(10, 0))
    # G = nx.compose(G, bipartite(10, 10))
    # G = nx.compose(G, star(10, 20))
    # G = nx.compose(G, king(10, 30))
    with open('../output/data.json', 'w') as f:
        graphs_json = []
        for G in graphs:
            graphs_json.append(json_graph.node_link_data(G))
        json.dump(graphs_json, f)