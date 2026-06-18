import networkx as nx

def shortest_path_demo():
    G = nx.Graph()
    edges = [
        ("A", "B", 4), ("A", "C", 2), ("B", "C", 1),
        ("B", "D", 5), ("C", "D", 8), ("C", "E", 10),
        ("D", "E", 2), ("D", "F", 6), ("E", "F", 3),
    ]
    G.add_weighted_edges_from(edges)
    path = nx.shortest_path(G, "A", "F", weight="weight")
    length = nx.shortest_path_length(G, "A", "F", weight="weight")
    tree = nx.minimum_spanning_tree(G, weight="weight")
    return path, length, list(tree.edges(data=True))

def max_flow_demo():
    G = nx.DiGraph()
    G.add_edge("s", "a", capacity=8)
    G.add_edge("s", "b", capacity=5)
    G.add_edge("a", "b", capacity=3)
    G.add_edge("a", "t", capacity=4)
    G.add_edge("b", "t", capacity=7)
    return nx.maximum_flow(G, "s", "t")

if __name__ == "__main__":
    print("shortest/mst:", shortest_path_demo())
    print("max flow:", max_flow_demo())
