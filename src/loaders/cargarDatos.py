from pathlib import Path
from src.modelos.grafo import Grafo

class CargarDatos:
    def __init__(self, ruta = None):
        if ruta is None:
            self.ruta = Path(__file__).resolve().parent.parent.parent / "data"
        else:
            self.ruta = Path(ruta)

    def leerConexiones(self, grafo):
        encabezado_saltado = False
        with open(self.ruta / "wiki-topcats.mtx", encoding= "utf-8") as arch:
            for linea in arch:

                linea = linea.strip()
                if not linea or linea.startswith("%"):
                    continue
                partes = linea.split()
            
                if not encabezado_saltado:
                    encabezado_saltado = True
                    continue
            
                id_origen = int(partes[0])
                id_destino = int(partes[1])
                grafo.agregarConexion(id_origen, id_destino)

    def leerNombresArticulos(self, grafo):
        with open(self.ruta / "wiki-topcats_pagenames.txt", encoding= "utf-8") as arch:
            for indice, linea in enumerate(arch, start = 1):
                if indice in grafo.articulos:
                    grafo.articulos[indice].nombre = linea.strip()
    
    def leerCategorias(self, grafo, categorias):
        with open(self.ruta / "wiki-topcats_Categories.mtx", encoding= "utf-8") as arch:
            for linea in arch:
                
                linea = linea.strip()
                partes = linea.split()
                
                if not linea or linea.startswith("%") or len(partes) == 3:
                    continue
                
                id_nodo = int(partes[0])
                id_categoria = int(partes[1])

                if id_nodo in grafo.articulos and id_categoria in categorias:
                    grafo.agregarCategoria(grafo.articulos[id_nodo], categorias[id_categoria])

    def leerNombresCategorias(self):
        categorias = {}
        
        with open(self.ruta / "wiki-topcats_Category_names.txt", encoding= "utf-8") as arch:
            for indice, linea in enumerate(arch, start = 1):
                nombre_categoria = linea.strip()
                categorias[indice] = nombre_categoria
    
        return categorias
    
    def cargarGrafo(self):
        grafo = Grafo()
        self.leerConexiones(grafo)
        self.leerNombresArticulos(grafo)
        nombres_categorias = self.leerNombresCategorias()
        self.leerCategorias(grafo, nombres_categorias)
        return grafo