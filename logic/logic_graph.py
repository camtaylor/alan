import networkx as nx
import matplotlib.pyplot as plt
import pylab



G = nx.DiGraph()


def connect(graph, from_node, to_node):
  graph.add_edge(from_node,to_node)


def display_graph(G):
  pos=nx.spring_layout(G)
  node_labels = {node:node for node in G.nodes()}
  nx.draw_networkx_labels(G, pos, labels=node_labels)
  nx.draw(G,pos)
  pylab.show()


def pos_insertion(pos_list):
  print pos_list
  G.add_edges_from(pos_list)
  G.add_edges_from([pos_tuple[::-1] for pos_tuple in pos_list])
  G.add_path([word[0] for word in pos_list])
  G.add_path([pos[1] for pos in pos_list])
  try:
    print nx.shortest_path(G,source=raw_input("Source:"),target=raw_input("Target:"))
  except Exception as e:
    print e
  display_graph(G)
 

def in_edges(node):
  return G.in_edges(node)


def out_edges(node):
  return G.out_edges(node)


if __name__ == "__main__":
  pos_insertion([('Alan', 'NNP'), ('is', 'VBZ'), ('the', 'DT'), ('name', 'NN'), ('of', 'IN'), ('a', 'DT'), ('computer', 'NN')])
