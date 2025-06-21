from model.modello import Model

mymodel = Model()
grafo = mymodel.buildGraph(1,5)
print(len(grafo.nodes), len(grafo.edges))
