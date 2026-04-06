from pathlib import Path
from src.grafo import Grafo

class CargarDatos:
    def __init__(self):
        self.ruta = Path(__file__).resolve().parent.parent / "data"

    def leerConexiones(self, grafo):
        with open(self.ruta / "wiki-topcats.mtx") as arch:
            for linea in arch:

                partes = linea.split(" ")
                
                if linea.startswith("%") or len(partes) == 3:
                    continue
                
                origen = int(partes[0])
                destino = int(partes[1])

                grafo.agregarConexion(origen, destino)

    def cargarGrafo(self):
        grafo = Grafo()
        self.leerConexiones(grafo)
        return grafo