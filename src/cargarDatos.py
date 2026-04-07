from pathlib import Path
from src.grafo import Grafo

class CargarDatos:
    def __init__(self):
        self.ruta = Path(__file__).resolve().parent.parent / "data"

    def leerConexiones(self, grafo, limite = 100000):
        print("Leyendo conexiones... (limite: {limite})...")
        cont = 0
        with open(self.ruta / "wiki-topcats.mtx") as arch:
            for linea in arch:

                partes = linea.split(" ")
                
                if linea.startswith("%") or len(partes) == 3:
                    continue
                
                origen = int(partes[0])
                destino = int(partes[1])

                grafo.agregarConexion(origen, destino)
                cont += 1
                if cont >= limite:
                    break
        print(f"Conexiones leídas: {cont}")

    def leerRelaciones(self, grafo): #Relacion Articulo - Categoria
        with open(self.ruta / "wiki-topcats_Categories.mtx") as arch:
            for linea in arch:
                
                linea = linea.strip()
                partes = linea.split(" ")
                
                if not linea or linea.startswith("%") or len(partes) == 3:
                    continue
                
                origen = int(partes[0])
                destino = int(partes[1])
            
                nodo = grafo.agregarNodo(origen)
                nodo.agregarCategoria(destino)

    def cargarNombresArticulos(self, grafo):
        with open(self.ruta / "wiki-topcats_pagenames.txt", "r", encoding="utf-8") as arch:
            for linea in arch:
                partes = linea.strip().split(" ", 1)
                if len(partes) == 2:
                    id_art = int(partes[0])
                    nombre = partes[1]
                    if id_art in grafo.articulos:
                        grafo.articulos[id_art].nombre = nombre


    def cargarGrafo(self):
        grafo = Grafo()
        self.leerConexiones(grafo)
        self.leerRelaciones(grafo)
        self.cargarNombresArticulos(grafo)
        return grafo
    
    def leerNombresArticulos(self):
        Nombres = {}
        
        with open(self.ruta / "wiki-topcats_pagenames.txt", encoding = "utf-8") as arch:
            for indice, linea in enumerate(arch, start = 1):
                Nombres[indice] = linea.strip()
        
        return Nombres
    
    def leerNombresCategorias(self):
        Categorias = {}
        
        with open(self.ruta / "wiki-topcats_Category_names.txt", encoding = "utf-8") as arch:
            for indice, linea in enumerate(arch, start = 1):
                Categorias[indice] = linea.strip()
                
        return Categorias