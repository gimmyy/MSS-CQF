import networkx as nx
class portGraph:
    def __init__(self, port):
       self.port = port
       self.graph = nx.Graph()