from src.modelos.nodo import Nodo
from collections import deque

class Grafo:
    def __init__(self):
        self.articulos = {}
        self.categorias = {}
    
    def agregarNodo(self, id):
        if id not in self.articulos:
            self.articulos[id] = Nodo(id)
        return self.articulos[id]
    
    def agregarConexion(self, idOrigen, idDestino):
        origen = self.agregarNodo(idOrigen)
        destino = self.agregarNodo(idDestino)
        origen.agregarEnlaceSalida(idDestino)
        destino.agregarEnlaceEntrada(idOrigen)

    def agregarCategoria(self, nodo, nombreCategoria):
        nodo.agregarCategoria(nombreCategoria)
        if nombreCategoria not in self.categorias:
            self.categorias[nombreCategoria] = []
        self.categorias[nombreCategoria].append(nodo)

    def cantidadArticulos(self):
        return len(self.articulos)
    
    def cantidadEnlaces(self):
        totalEnlaces = 0
        
        for nodo in self.articulos.values():
            totalEnlaces += nodo.gradoSalida()
        
        return totalEnlaces

    def resumen(self):
        return {"Articulos": self.cantidadArticulos(), 
                "Enlaces": self.cantidadEnlaces()}

    def topPorGradoEntrada(self, cantidad = 10):
        lista = list(self.articulos.values())
        lista.sort(key = lambda nodo: nodo.gradoEntrada(), reverse = True)
        return lista[:cantidad]
    
    def topPorGradoSalida(self, cantidad = 10):
        lista = list(self.articulos.values())
        lista.sort(key = lambda nodo: nodo.gradoSalida(), reverse = True)
        return lista[:cantidad]
    
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
        
        for grad in grados_ordenados[:10]:
            cantidad = distri[grad]
            porcentaje = (cantidad / nodos_totales) * 100
            print(f"Grado: {grad}, Cantidad articulos: {cantidad}, Porcentaje: {porcentaje:.2f}%")
        
        grado_maximo =  grados_ordenados[-1]
        print(f"Grado maximo: {grado_maximo}, Cantidad articulos: {distri[grado_maximo]}")
        return distri
    
    def bfs(self, idInicio):
        
        if idInicio not in self.articulos:
            return []
        
        visitados = set()
        cola = deque([idInicio])
        ordenVisita = []
        
        while cola:
            actual = cola.popleft()
            
            if actual not in visitados:
                visitados.add(actual)
                ordenVisita.append(actual)
                
                for vecino in self.articulos[actual].enlacesSalida:
                    if vecino not in visitados:
                        cola.append(vecino)
        
        return ordenVisita
    
    
    def dfs(self, idInicio):
        
        if idInicio not in self.articulos:
            return[]
        
        visitados = set()
        pila = [idInicio]
        ordenVisita = []
        
        while pila:
            actual = pila.pop()
            
            if actual not in visitados:
                visitados.add(actual)
                ordenVisita.append(actual)
                
                vecinos = list(self.articulos[actual].enlacesSalida)
                vecinos.sort()
                vecinos.reverse()
                
                for vecino in vecinos:
                    if vecino not in visitados:
                        pila.append(vecino)
                        
        return ordenVisita
    
    #Funcion relacionada a exploracion de conectividad entre articulos
    def esAlcanzable(self, idOrigen, idDestino): #Ver si de un articulo se puede llegar a otro
        
        if idOrigen not in self.articulos or idDestino not in self.articulos:
            return False
        
        visitados = set()
        cola = deque([idOrigen])
        
        while cola:
            actual = cola.popleft()
            
            if actual == idDestino:
                return True

            for vecino in self.articulos[actual].enlacesSalida:
                if vecino not in visitados:
                    visitados.add(vecino)
                    cola.append(vecino)
        
        return False
    
    #Temporal: Falta aplicarle mejoras para encontrar caminos mas interesantes
    def encontrarCaminosSimples(self, idOrigen, idDestino): 
        
        if idOrigen not in self.articulos or idDestino not in self.articulos:
            return []
        
        cola = deque([idOrigen])
        padres = {idOrigen : None}
        
        while cola:
            actual = cola.popleft()
            
            if actual == idDestino:
                break
            
            for vecino in self.articulos[actual].enlacesSalida:
                if vecino not in padres:
                    padres[vecino] = actual
                    cola.append(vecino)
                    
        if idDestino not in padres:
            return []
        
        camino = []
        actual = idDestino

        while actual is not None:
            camino.append(actual)
            actual = padres[actual]
        
        camino.reverse()
        
        return camino
    
    #PageRank
    def pageRank(self, iteraciones = 20, damping = 0.85):
        cantidadNodos = len(self.articulos)
        
        if cantidadNodos == 0:
            return {}
        
        puntajes = {}
        valorInicial = 1.0 / cantidadNodos
        
        for idNodo in self.articulos:
            puntajes[idNodo] = valorInicial
        
        for _ in range(iteraciones):
            nuevosPuntajes = {}
            
            for idNodo in self.articulos:
                nuevosPuntajes[idNodo] = (1.0 - damping) / cantidadNodos
            
            for idNodo, nodo in self.articulos.items():
                
                if nodo.gradoSalida() == 0:
                    continue
                
                aporte = puntajes[idNodo] / nodo.gradoSalida()
                
                for vecino in nodo.enlacesSalida:
                    nuevosPuntajes[vecino] += damping * aporte
                
            puntajes = nuevosPuntajes
        
        return puntajes
    # Relacion de las categorias con los articulos mas importantes
    def ranking_categorias(self, puntajes_pagerank, top_n=10):
        cat_stats = {} 
    
        for id_art, articulo in self.articulos.items():
            score = puntajes_pagerank.get(id_art, 0)
            for categoria in articulo.categorias:
                if categoria not in cat_stats:
                    cat_stats[categoria] = []
                cat_stats[categoria].append(score)
                
        ranking = []
        for nombre_cat, scores in cat_stats.items():
            promedio = sum(scores) / len(scores) if scores else 0
            ranking.append((nombre_cat, promedio, len(scores)))
            
        ranking.sort(key=lambda x: x[1], reverse=True)
        return ranking[:top_n]
    
    #SubGrafo para guardar solo lo relacionado a futbol
    def subGrafoFutbol(self):
        subGrafo = Grafo()
        articulos_validos = set()
        
        for idNodo, nodo in self.articulos.items():
            for categoria in nodo.categorias:
                if self.esCategoriaFutbol(categoria):
                    articulos_validos.add(idNodo)
                    break
                
        for idNodo in articulos_validos:
            nodoOriginal = self.articulos[idNodo]
            nuevoNodo = subGrafo.agregarNodo(idNodo)
            nuevoNodo.nombre = nodoOriginal.nombre
            
            for categoria in nodoOriginal.categorias:
                nuevoNodo.agregarCategoria(categoria)
                
        for idNodo in articulos_validos:
            nodoOriginal = self.articulos[idNodo]
            
            for vecino in nodoOriginal.enlacesSalida:
                if vecino in articulos_validos:
                    subGrafo.agregarConexion(idNodo, vecino)
                    
        return subGrafo

    def esCategoriaFutbol(self, nombre):
        palabras_futbol = ["fifa", "uefa", "world_cup", "premier_league",
                        "la_liga", "serie_a", "bundesliga", "soccer", "football_club"]
        nombre = nombre.lower()
        
        for palabra in palabras_futbol:
            if palabra in nombre:
                return True
            
        return False