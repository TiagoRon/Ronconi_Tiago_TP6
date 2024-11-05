from grafo import Graph  # Asume que `grafo.py` contiene la implementación base de Graph.
from heap import HeapMin

class Maravilla:
    def __init__(self, nombre, pais, tipo):
        self.nombre = nombre
        self.pais = pais if isinstance(pais, list) else [pais]
        self.tipo = tipo

class GrafoMaravillas(Graph):
    def __init__(self):
        super().__init__(dirigido=False)
    
    def insertar_maravilla(self, nombre, pais, tipo):
        self.insert_vertice(nombre)
        for nodo in self.elements:
            if nodo['value'] == nombre:
                nodo['pais'] = pais
                nodo['tipo'] = tipo

    def insertar_conexiones(self, tipo):
        for i, nodo1 in enumerate(self.elements):
            if nodo1['tipo'] == tipo:
                for j, nodo2 in enumerate(self.elements[i+1:], start=i+1):
                    if nodo2['tipo'] == tipo:
                        # Distancia puede depender de datos predefinidos o ser generada aleatoriamente para esta demostración
                        distancia = 100  # Placeholder para la distancia
                        self.insert_arista(nodo1['value'], nodo2['value'], distancia)

    def arbol_expansion_minimo(self, tipo):
        grafo_filtrado = [nodo for nodo in self.elements if nodo['tipo'] == tipo]
        if not grafo_filtrado:
            print("No hay maravillas de tipo", tipo)
            return None
        return self.kruskal(grafo_filtrado[0]['value'])

    def existen_maravillas_naturales_y_arquitectonicas(self):
        paises_naturales = set()
        paises_arquitectonicas = set()
        for nodo in self.elements:
            if nodo['tipo'] == 'natural':
                paises_naturales.update(nodo['pais'])
            elif nodo['tipo'] == 'arquitectonica':
                paises_arquitectonicas.update(nodo['pais'])
        return paises_naturales & paises_arquitectonicas

    def pais_con_multiples_maravillas_mismo_tipo(self):
        paises_contador = {}
        for nodo in self.elements:
            for pais in nodo['pais']:
                if pais not in paises_contador:
                    paises_contador[pais] = {'natural': 0, 'arquitectonica': 0}
                paises_contador[pais][nodo['tipo']] += 1
        return {pais: tipos for pais, tipos in paises_contador.items() if max(tipos.values()) > 1}

# Ejemplo de uso:
if __name__ == "__main__":
    grafo_maravillas = GrafoMaravillas()
    # Agregar maravillas - nombres de ejemplo
    grafo_maravillas.insertar_maravilla("Taj Mahal", "India", "arquitectonica")
    grafo_maravillas.insertar_maravilla("Machu Picchu", "Perú", "arquitectonica")
    grafo_maravillas.insertar_maravilla("Cristo Redentor", "Brasil", "arquitectonica")
    # Agregar más maravillas según los datos...

    # Conectar maravillas
    grafo_maravillas.insertar_conexiones("arquitectonica")
    grafo_maravillas.insertar_conexiones("natural")

    # Árbol de expansión mínimo para cada tipo de maravillas
    print("Árbol de expansión mínimo (arquitectónicas):", grafo_maravillas.arbol_expansion_minimo("arquitectonica"))
    print("Árbol de expansión mínimo (naturales):", grafo_maravillas.arbol_expansion_minimo("natural"))

    # ¿Existen países con maravillas de ambos tipos?
    print("Países con maravillas naturales y arquitectónicas:", grafo_maravillas.existen_maravillas_naturales_y_arquitectonicas())

    # ¿Algún país tiene múltiples maravillas del mismo tipo?
    print("Paises con múltiples maravillas del mismo tipo:", grafo_maravillas.pais_con_multiples_maravillas_mismo_tipo())
