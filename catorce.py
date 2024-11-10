from cola import Queue
from heap import HeapMin
from pila import Stack

class Graph:
    def __init__(self, dirigido=True):
        self.elements = []
        self.dirigido = dirigido

    def show_graph(self):
        print("\nNodos:")
        for nodo in self.elements:
            print(nodo['value'])
            print("    Aristas:")
            for arista in nodo['aristas']:
                print(f"    destino: {arista['value']} peso: {arista['peso']}")
        print()

    def search(self, value):
        for index, element in enumerate(self.elements):
            if element['value'] == value:
                return index
        return None

    def insert_vertice(self, value):
        nodo = {
            'value': value,
            'aristas': [],
            'visitado': False,
        }
        self.elements.append(nodo)

    def insert_arista(self, origen, destino, peso):
        pos_origen = self.search(origen)
        pos_destino = self.search(destino)
        if pos_origen is not None and pos_destino is not None:
            arista = {'value': destino, 'peso': peso}
            self.elements[pos_origen]['aristas'].append(arista)
            if not self.dirigido:
                arista = {'value': origen, 'peso': peso}
                self.elements[pos_destino]['aristas'].append(arista)

    def mark_as_not_visited(self):
        for nodo in self.elements:
            nodo['visitado'] = False

    def dijkstra(self, origen):
        from math import inf
        no_visitados = HeapMin()
        camino = {}
        for nodo in self.elements:
            distancia = 0 if nodo['value'] == origen else inf
            no_visitados.arrive([nodo['value'], nodo, None], distancia)
            camino[nodo['value']] = distancia
        while len(no_visitados.elements) > 0:
            node = no_visitados.atention()
            costo_nodo_actual = node[0]
            adjacentes = node[1][1]['aristas']
            for adjacente in adjacentes:
                pos = no_visitados.search(adjacente['value'])
                if pos is not None:
                    if costo_nodo_actual + adjacente['peso'] < no_visitados.elements[pos][0]:
                        no_visitados.change_proirity(pos, costo_nodo_actual + adjacente['peso'])
                        camino[adjacente['value']] = costo_nodo_actual + adjacente['peso']
        return camino

    def kruskal(self):
        def buscar_en_bosque(bosque, buscado):
            for index, arbol in enumerate(bosque):
                if buscado in arbol:
                    return index
            return None

        bosque = [[nodo['value']] for nodo in self.elements]
        aristas = HeapMin()
        for nodo in self.elements:
            adjacentes = nodo['aristas']
            for adjacente in adjacentes:
                aristas.arrive([nodo['value'], adjacente['value']], adjacente['peso'])

        arbol_expansion = []
        while len(bosque) > 1 and len(aristas.elements) > 0:
            arista = aristas.atention()
            origen = buscar_en_bosque(bosque, arista[1][0])
            destino = buscar_en_bosque(bosque, arista[1][1])
            if origen is not None and destino is not None and origen != destino:
                arbol_expansion.append(arista)
                bosque[origen].extend(bosque[destino])
                bosque.pop(destino)
        return arbol_expansion

grafo = Graph(dirigido=False)
ambientes = [
    "cocina", "comedor", "cochera", "quincho",
    "bano 1", "bano 2", "habitacion 1", "habitacion 2",
    "sala de estar", "terraza", "patio"
]

for ambiente in ambientes:
    grafo.insert_vertice(ambiente)

grafo.insert_arista("cocina", "comedor", 3)
grafo.insert_arista("cocina", "terraza", 4)
grafo.insert_arista("cocina", "patio", 5)
grafo.insert_arista("comedor", "sala de estar", 7)
grafo.insert_arista("comedor", "bano 1", 2)
grafo.insert_arista("comedor", "patio", 6)
grafo.insert_arista("sala de estar", "habitacion 1", 8)
grafo.insert_arista("sala de estar", "habitacion 2", 3)
grafo.insert_arista("patio", "terraza", 4)
grafo.insert_arista("patio", "quincho", 5)
grafo.insert_arista("habitacion 1", "habitacion 2", 2)

arbol_minimo = grafo.kruskal()
print("Arbol de expansion minima:", arbol_minimo)

distancias = grafo.dijkstra("habitacion 1")
print("Distancia minima desde habitacion 1 hasta sala de estar:", distancias["sala de estar"], "metros")
