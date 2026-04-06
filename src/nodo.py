
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
        return len(self.gradoEntrada)
    
    def gradoSalida(self):
        return len(self.enlacesSalida)  