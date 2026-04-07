
class Nodo:
    def __init__(self, id):
        self.id = id
        self.nombre = None
        self.categorias = set()
        self.enlacesSalida = set()
        self.enlacesEntrada = set()
    
    def agregarEnlaceEntrada(self, idOrigen):
        self.enlacesEntrada.add(idOrigen)
    
    def agregarEnlaceSalida(self, idDestino):
        self.enlacesSalida.add(idDestino)

    def agregarCategoria(self, categoria):
        self.categorias.add(categoria)

    def gradoEntrada(self):
        return len(self.enlacesEntrada)
    
    def gradoSalida(self):
        return len(self.enlacesSalida)  
    
    def __str__(self):
        if self.nombre:
            return f"Nodo con id={self.id} y nombre={self.nombre})"
        else:
            return f"Nodo con id={self.id} y sin nombre)"
    