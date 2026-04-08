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
        origen.agregarEnlaceSalida(idDestino)
        destino.agregarEnlaceEntrada(idOrigen)

    def obtenerMayoresConexiones(self, n =10):
        lista_grados_enlaces =  []
        for nodo in self.articulos.values():
            lista_grados_enlaces.append([nodo.gradoEntrada(), nodo])
        
        lista_grados_enlaces.sort(reverse = True)
        lista_resultado = []
        
        for grado, nodo in lista_grados_enlaces:
            lista_resultado.append(nodo)
        return lista_resultado[:n]
