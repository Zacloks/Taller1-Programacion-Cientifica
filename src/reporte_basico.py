from pathlib import Path

class reporteBasico:
    
    def __init__(self, carpetaResultados = None):
        if carpetaResultados is None:
            self.carpetaResultados = Path(__file__).resolve().parent.parent / "results"
        else:
            self.carpetaResultados = Path(carpetaResultados)

    def generar(self, grafo):
        self.carpetaResultados.mkdir(parents = True, exist_ok = True)
        
        resumenGrafo = grafo.resumen()
        topEntrada = self.extraerTop(grafo.topPorGradoEntrada(5), "entrada")
        topSalida = self.extraerTop(grafo.topPorGradoSalida(5), "salida")
        
        rutaTexto = self.carpetaResultados / "reporte_basico.txt"
        
        return {"texto": rutaTexto}
    
    def extraerTop(self, articulos, tipoGrado):
        top = []
        
        for articulo in articulos:
            if tipoGrado == "entrada":
                valor = articulo.gradoEntrada()
            else:
                valor = articulo.gradoSalida()
            
            top.append({"nombre": articulo.nombre,
                       "Valor": valor})
              
        return top
    
    def imprimirTop(self, titulo, items):
        print()
        print(titulo)
        print("-" * titulo)
        
        for posicion, item in enumerate(items, start = 1):
            print(f"{posicion}. {item["nombre"]} -> {item["valor"]}")
    