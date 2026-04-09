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

    def obtenerMayoresConexiones(self, n =10, tipo = "entrada"):
        lista_grados_enlaces =  []
        for nodo in self.articulos.values():
            
            if tipo == "entrada":
                valor = nodo.gradoEntrada()
            else:
                valor = nodo.gradoSalida()
            lista_grados_enlaces.append([valor, nodo])
        
        lista_grados_enlaces.sort(key = lambda x: x[0], reverse = True)
        lista_resultado = []

        for grado, nodo in lista_grados_enlaces[:n]:
            lista_resultado.append(nodo)
        return lista_resultado

    def analizarDistribucionGrados(self, tipo = "entrada"):
        distri = {}
        nodos_totales = len(self.articulos)

        if nodos_totales == 0:
            return "El grafo esta vacio, no hay datos"
        
        for nodo in self.articulos.values():
            if tipo == "entrada":
                grado_actual = nodo.gradoEntrada()
            else:
                grado_actual = nodo.gradoSalida()
            distri[grado_actual] = distri.get(grado_actual,0) +1

        grados_ordenados = list(distri.keys())
        grados_ordenados.sort()

        print(f"---Distribución:---")
        print(f"Cantidad de Articulos analizados: {nodos_totales}")
        
        for grad in grados_ordenados[:10]:
            cantidad = distri[grad]
            porcentaje = (cantidad / nodos_totales) * 100
            print(f"Grado: {grad}, Cantidad articulos: {cantidad}, Porcentaje: {porcentaje:.2f}%")
        
        grado_maximo =  grados_ordenados[-1]
        print(f"Grado maximo: {grado_maximo}, Cantidad articulos: {distri[grado_maximo]}")
        return distri