from pathlib import Path
from src.grafo import Grafo

class CargarDatos:
    def __init__(self):
        self.ruta = Path(__file__).resolve().parent.parent / "data"

    def leerConexiones(self, grafo):
        with open(self.ruta / "wiki-topcats.mtx") as arch:
            for linea in arch:

                linea = linea.strip()

                if not linea or linea.startswith("%"):
                    continue

                partes = linea.split()

                if len(partes) == 3:
                    continue
                
                origen = int(partes[0])
                destino = int(partes[1])

                grafo.agregarConexion(origen, destino)

    def leerNombresArticulos(self, grafo):
        with open(self.ruta / "wiki-topcats_pagenames.txt", encoding = "utf-8") as arch:
            for indice, linea in enumerate(arch, start = 1):
                if indice in grafo.articulos:   #Temporal  
                    grafo.articulos[indice].nombre = linea.strip()
    
    def leerCategorias(self, grafo):
        with open(self.ruta / "wiki-topcats_Categories.mtx") as arch:
            for linea in arch:
                
                linea = linea.strip()
                partes = linea.split()
                
                if not linea or linea.startswith("%") or len(partes) == 3:
                    continue
                
                id_nodo = int(partes[0])
                categoria = int(partes[1])   

                if id_nodo in grafo.articulos:  #Temporal       
                    grafo.articulos[id_nodo].agregarCategoria(categoria)

    def leerNombresCategorias(self):
        categorias = {}
        
        with open(self.ruta / "wiki-topcats_Category_names.txt", encoding = "utf-8") as arch:
            for indice, linea in enumerate(arch, start = 1):
                categorias[indice] = linea.strip()
    
        return categorias
    
    def cargarGrafo(self):
        grafo = Grafo()
        self.leerConexiones(grafo)
        self.leerNombresArticulos(grafo)
        self.leerCategorias(grafo)
        categorias = self.leerNombresCategorias()
        return grafo