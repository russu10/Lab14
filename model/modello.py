import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.stores = DAO.getAllStores()
        self.grafo = None
        self.idMap = {}
        self.pesoMax = 0
        self.percorsoTop = []

    def buildGraph(self,store_id,k):
        grafo = nx.DiGraph()
        ordini = DAO.getAllOrders(store_id)
        grafo.add_nodes_from(ordini)
        archi = DAO.getAllArchi(store_id,k)
        for o in ordini:
            self.idMap[o.order_id] = o
        for a in archi:
            grafo.add_edge(self.idMap[a.id1],self.idMap[a.id2], peso = a.peso)

        self.grafo = grafo


        return grafo

    def cercaPercorsoLungo(self,id_nodo):
        nodo = self.idMap[int(id_nodo)]
        percorso_max = []
        tree = nx.dfs_tree(self.grafo, nodo)
        nodi = list(tree.nodes())
        for n in nodi:
            tmp = [n]
            while tmp[0] != nodo:
                predecessori = nx.predecessor(tree,nodo,tmp[0])
                tmp.insert(0,predecessori[0])
                if len(tmp) > len(percorso_max):
                    percorso_max = copy.deepcopy(tmp)
        return percorso_max

    def getPesoMax(self,id_nodo):
        nodo = self.idMap[int(id_nodo)]
        self.pesoMax = 0
        self.percorsoTop = []
        parziale = [nodo]
        vicini = self.grafo.neighbors(nodo)
        for v in vicini:
            parziale.append(v)
            self.ricorsione(parziale)
            parziale.pop()
        return self.pesoMax , self.percorsoTop

    def ricorsione(self,parziale):
        if self.calcolaPunteggio(parziale) > self.pesoMax:
            self.pesoMax = self.calcolaPunteggio(parziale)
            self.percorsoTop = copy.deepcopy(parziale)

        for v in self.grafo.neighbors(parziale[-1]):
            if (v not in parziale and
                    self.grafo[parziale[-2]][parziale[-1]]["peso"] >
                    self.grafo[parziale[-1]][v]["peso"]):
                parziale.append(v)
                self.ricorsione(parziale)
                parziale.pop()


    def calcolaPunteggio(self,parziale):
        peso =0
        for i in range(len(parziale)-1):
            peso += self.grafo[parziale[i]][parziale[i+1]]["peso"]
        return peso
