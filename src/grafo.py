from src.nodo import Nodo

class Grafo:
    def __init__(self):
        self.articulos = {}
    
    def agregarNodo(self, id):
        if id not in self.articulos:
            self.articulos[id] = Nodo(id)
        return self.articulos[id]
    
    def agregarConexion(self, idOrigen, idDestino):
        origen = self.agregarNodo(idOrigen)
        destino = self.agregarNodo(idDestino)
        origen.agregarEnlaceSalida(self.agregarNodo(idOrigen))
        destino.agregarEnlaceEntrada(self.agregarNodo(idDestino))