import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDStrores(self):
        stores = self._model.stores
        for s in stores:
            self._view._ddStore.options.append(ft.dropdown.Option(key = s.store_id, text = s.store_name ))

        self._view.update_page()

    def handleCreaGrafo(self, e):
        id = self._view._ddStore.value
        k = self._view._txtIntK.value
        if id == None or k == None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire Store e valore massimo K"))
            self._view.update_page()
            return
        try :
            idInt = int(id)
            kInt = int(k)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire un valore valido di K"))
            self._view.update_page()
            return

        grafo = self._model.buildGraph(idInt,kInt)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato con {len(grafo.nodes)} nodi"
                                                      f" e {len(grafo.edges)} archi"))
        self._view._ddNode.options = []
        for nodo in grafo.nodes:

            self._view._ddNode.options.append(ft.dropdown.Option(nodo.order_id))
        self._view._btnCerca.disabled = False
        self._view.update_page()


    def handleCerca(self, e):
        id_nodo = self._view._ddNode.value
        if id_nodo == None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Inserire nodo desiderato"))
            self._view.update_page()
            return
        percorsoLungo = self._model.cercaPercorsoLungo(id_nodo)
        self._view.txt_result.controls.clear()
        for n in percorsoLungo:

            self._view.txt_result.controls.append(ft.Text(f" Nodo : {n.order_id}"))
        self._view._btnRicorsione.disabled = False
        self._view.update_page()

    def handleRicorsione(self, e):
        pesoMax , percorso = self._model.getPesoMax(int(self._view._ddNode.value))
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Percorso trovato"))
        for p in percorso:
            self._view.txt_result.controls.append(ft.Text(f"Nodo : {p.order_id}"))

        self._view.txt_result.controls.append(ft.Text(f"Con peso : {pesoMax}"))
        self._view.update_page()

