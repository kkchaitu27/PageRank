import networkx as nx
import matplotlib.pyplot as plt
import csv


def draw_graph(file):
    # create networkx graph
    G=nx.DiGraph()

    #Open File and read directed Edges from each line
    with open(file) as f:
        reader = csv.reader(f)
    	for row in reader:
           G.add_edge(row[0], row[1])

    #using shell layout
    graph_pos = nx.shell_layout(G)

    # draw nodes, edges and labels
    nx.draw_networkx_nodes(G, graph_pos, node_size=1000, node_color='blue', alpha=0.25)
    nx.draw_networkx_edges(G, graph_pos, width=2, alpha=0.25, edge_color='green')
    nx.draw_networkx_labels(G, graph_pos, font_size=12, font_family='sans-serif')

    # show graph
    plt.show()

draw_graph("directedEdges.csv")

