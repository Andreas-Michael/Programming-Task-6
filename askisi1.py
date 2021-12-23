import random
from random import choice
import networkx as nx
import matplotlib.pyplot as plt

class Node(object):
     """
         Undefined    = 0
         Susceptible = 1
         Infected    = 2
         Recovered    = 3
     """

     def __init__(self):
         self.state = 1
         self.nextState = 0

     def changeState(self):
         if self.nextState != 0:
             self.state = self.nextState
             self.nextState = 0

     def infectNode(self, nextNode, p):
         if nextNode.state != 1:
             return

         if random.random() <= p:
             nextNode.nextState = 2

     def decideHealing(self, q):
         if self.state != 2:
             return
         if random.random() <= q:
             self.nextState = 3

p_vals = [0.001, 0.002, 0.003, 0.008, 0.01, 0.05, 0.08, 0.10]
kinds_of_network = [1, 2]

number_of_nodes = 1000
edges_per_node = 3
initial_I_perc = 0.01
timeslots = 50
#p = 0.3
q = 0.01    # pithanotita anarrosis arrostou komvou

for network in kinds_of_network:
     for p in p_vals: # pithanotita molinsis se igii komvo
         G = nx.Graph()
         # k = p * (n-1)
         # p = 3 / 999

         array1 = []
         array2 = []
         array3 = []

         #dimiourgia komvon
         for i in range(number_of_nodes):
             node = Node();
             G.add_node(node);

         #dimiourgia sindeseon
         if network == 1:
             title = 'Random network'
             while G.number_of_edges() < edges_per_node * number_of_nodes:
                 n1 = choice(list(G.nodes()))
                 n2 = choice(list(G.nodes()))
                 if n1 != n2 and not n1 in G.neighbors(n2):
                     G.add_edge(n1, n2)
         else: # barabasi
             title = 'Barabasi/Albert network'
             core1 = []
             core2 = []

             for i in range(20):
                 n1 = choice(list(G.nodes()))
                 n2 = choice(list(G.nodes()))
                 if n1 not in core1:
                     core1.append(n1)
                 if n2 not in core2:
                     core2.append(n2)
             print("BA phase 1");
             # connect nodes in cores
             for n1 in core1:
                 for n2 in core1:
                     if n1 not in G.neighbors(n2):
                         G.add_edge(n1, n2)
             print("BA phase 2");
             for n1 in core2:
                 for n2 in core2:
                     if n1 not in G.neighbors(n2):
                         G.add_edge(n1, n2)
             print("BA phase 3");
             while G.number_of_edges() < edges_per_node * number_of_nodes:
                 for n1 in G.nodes():
                     if n1 not in core1 and n1 not in core2:
                         n2 = choice(list(G.nodes()))
                         if n1 != n2 and n1 not in G.neighbors(n2):
                             if random.random() <= (G.degree(n2) / 
G.number_of_edges()):
                                 G.add_edge(n1, n2)
                                 if G.number_of_edges() % 150 == 0:
                                     print("Edges: %d/%d" % 
(G.number_of_edges(), edges_per_node * number_of_nodes))
             print("BA phase 4");


         #dimiourgia arroston
         i = 0
         while i < initial_I_perc * number_of_nodes:
             n = choice(list(G.nodes()))
             if n.state == 1:
                 n.state = 2
                 i = i + 1

         # print("Edges", G.number_of_edges())

         timeslot = 0
         while timeslot < timeslots:
             healthy = 0
             ill = 0
             saved = 0
             for n in G.nodes():
                 if n.state == 1:
                     nextNodes = G.neighbors(n)
                     for nextNode in nextNodes:
                         if nextNode.state == 2:
                             nextNode.infectNode(n, p)
                     healthy = healthy + 1
                 elif n.state == 2:
                     n.decideHealing(q)
                     ill = ill + 1
                 else:
                     saved = saved + 1

             array1.append(healthy)
             array2.append(ill)
             array3.append(saved)

             timeslot = timeslot + 1

             for n in G.nodes():
                 n.changeState()

         timeline = []
         for i in range(timeslots):
             timeline.append(i+1)



         plt.xlabel('time')
         plt.ylabel('nodes')
         plt.plot(timeline, array1, label = 'Susceptible')
         plt.plot(timeline, array2, label = 'Infected')
         plt.plot(timeline, array3, label = 'Recovered')
         plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=3, 
mode="expand", borderaxespad=0.)
         plt.suptitle('%s, p=%0.1f, q=%0.1f, p/q=%0.1f' % (title, p , q, 
p/q))

         plt.show()
