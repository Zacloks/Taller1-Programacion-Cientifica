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

    def analizarDistribucionGrados(self, tipo="entrada"):
        distri = {}
        nodos_totales = len(self.articulos)

        if nodos_totales == 0:
            return {}
        
        for nodo in self.articulos.values():
            grado_actual = nodo.gradoEntrada() if tipo == "entrada" else nodo.gradoSalida()
            distri[grado_actual] = distri.get(grado_actual, 0) + 1

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
    
    def esAlcanzable(self, idOrigen, idDestino):
        
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
    
    def encontrarCamino(self, idOrigen, idDestino): 
        
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
    
    #Analisis futbol
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
                subGrafo.agregarCategoria(nuevoNodo, categoria)  # ← corregido
                
        for idNodo in articulos_validos:
            nodoOriginal = self.articulos[idNodo]
            for vecino in nodoOriginal.enlacesSalida:
                if vecino in articulos_validos:
                    subGrafo.agregarConexion(idNodo, vecino)
                    
        return subGrafo

    def esCategoriaFutbol(self, nombre):
        palabras_futbol = ["fifa", "uefa", "world_cup", "premier_league",
                "la_liga", "serie_a", "bundesliga", "soccer", "football_club",
                "footballer", "football_player", "association_football",
                "copa_america", "champions_league"]
        nombre = nombre.lower()
        
        return any(palabra in nombre for palabra in palabras_futbol)

    def quienPuedeLlegarA(self, idDestino):
        visitados = set()
        cola = deque([idDestino])
        
        while cola:
            actual = cola.popleft()
            if actual not in visitados:
                visitados.add(actual)
                for vecino in self.articulos[actual].enlacesEntrada:
                    if vecino not in visitados:
                        cola.append(vecino)
        
        return visitados

    def buscarPorNombre(self, nombre):
        for id_nodo, nodo in self.articulos.items():
            if nodo.nombre == nombre:
                return id_nodo
        return None

    def topFutbolistasPorPageRank(self, puntajes_pagerank, top_n=10):
        categorias_jugadores = [cat for cat in self.categorias 
                                if cat.endswith("_footballers")
                                and not cat.startswith("Expatriate")
                                and not cat.startswith("Olympic")]
        
        futbolistas = set()
        for cat in categorias_jugadores:
            for nodo in self.categorias[cat]:
                futbolistas.add(nodo.id)
        
        ranking = []
        for id_nodo in futbolistas:
            score = puntajes_pagerank.get(id_nodo, 0)
            nodo = self.articulos[id_nodo]
            ranking.append((nodo.nombre, score, id_nodo))
        
        ranking.sort(key=lambda x: x[1], reverse=True)
        return ranking[:top_n]

    def categoriasFutbolMasGrandes(self, top_n=10):
        cats_futbol = {cat: nodos for cat, nodos in self.categorias.items() 
                    if self.esCategoriaFutbol(cat)}
        ranking = sorted(cats_futbol.items(), key=lambda x: len(x[1]), reverse=True)
        return [(nombre, len(nodos)) for nombre, nodos in ranking[:top_n]]

    def categoriasFutbolMasInfluyentes(self, puntajes_pagerank, top_n=10):
        cats_futbol = {cat: nodos for cat, nodos in self.categorias.items() 
                    if self.esCategoriaFutbol(cat)}
        ranking = []
        for nombre_cat, nodos in cats_futbol.items():
            scores = [puntajes_pagerank.get(n.id, 0) for n in nodos]
            promedio = sum(scores) / len(scores) if scores else 0
            ranking.append((nombre_cat, promedio, len(nodos)))
        ranking.sort(key=lambda x: x[1], reverse=True)
        return ranking[:top_n]

    def compararPageRankLocalVsGlobal(self, puntajes_global, puntajes_local, top_n=10):
        comparacion = []
        for id_nodo in self.articulos:
            score_local = puntajes_local.get(id_nodo, 0)
            score_global = puntajes_global.get(id_nodo, 0)
            nodo = self.articulos[id_nodo]
            comparacion.append((nodo.nombre, score_global, score_local))
        
        por_local = sorted(comparacion, key=lambda x: x[2], reverse=True)[:top_n]
        return por_local