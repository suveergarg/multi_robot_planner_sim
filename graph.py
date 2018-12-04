import networkx as nx
import matplotlib.pyplot as plt
import pygraphviz as pgv

def create_graph():
	G= nx.DiGraph()

	for i in range(100):
		G.add_node(i+1)

	for i in range(1,91):
		if i%2 == 0:
			G.add_edge(i,i+10)
		else :
			G.add_edge(i+10,i)


	for j in range(10):
		for i in range(1,10):
			if j%2==0 :
				G.add_edge((j*10)+i,(j*10)+i+1)
			else :	
				G.add_edge((j*10)+i+1,(j*10)+i)

	A = nx.nx_agraph.to_agraph(G)
	A.layout()
	A.draw('layout.png')
	return G
