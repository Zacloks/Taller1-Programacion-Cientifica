from pathlib import Path

class ReporteBasico:
    
    def __init__(self, carpetaResultados = None):
        if carpetaResultados is None:
            self.carpetaResultados = Path(__file__).resolve().parent.parent.parent / "results"
        else:
            self.carpetaResultados = Path(carpetaResultados)

    def generar(self, grafo):
        self.carpetaResultados.mkdir(parents = True, exist_ok = True)
        
        resumenGrafo = grafo.resumen()
        topEntrada = self.extraerTop(grafo.topPorGradoEntrada(5), "entrada")
        topSalida = self.extraerTop(grafo.topPorGradoSalida(5), "salida")
        
        rutaTexto = self.carpetaResultados / "reporte_basico.txt"
        self.exportarTexto(rutaTexto, resumenGrafo, topEntrada, topSalida)
        
        return {"texto": rutaTexto}
    
    def extraerTop(self, articulos, tipoGrado):
        top = []
        
        for articulo in articulos:
            if tipoGrado == "entrada":
                valor = articulo.gradoEntrada()
            else:
                valor = articulo.gradoSalida()
            
            top.append({"nombre": articulo.nombre,
                       "valor": valor})
              
        return top
    
    def imprimirTop(self, titulo, items):
        print()
        print(titulo)
        print("-" * len(titulo))
        
        for posicion, item in enumerate(items, start = 1):
            print(f"{posicion}. {item['nombre']} -> {item['valor']}")
    
    def imprimirPorConsola(self, grafo):
        resumenGrafo = grafo.resumen()
        
        topEntrada = self.extraerTop(grafo.topPorGradoEntrada(10), "entrada")
        topSalida = self.extraerTop(grafo.topPorGradoSalida(10), "salida")
        
        print("===Resumen del Grafo===")
        print(f"Cantidad de Articulos: {resumenGrafo['Articulos']}")
        print(f"Cantidad de Enlaces: {resumenGrafo['Enlaces']}")
        
        self.imprimirTop("Top 10 por grado de Entrada", topEntrada)
        self.imprimirTop("Top 10 por grados de Salida", topSalida)
        
    def exportarTexto(self, rutaSalida, resumen, topEntrada, topSalida):
        lineas = ["Reporte Basico de Wikipedia",
                  "",
                  f"Cantidad de Articulos: {resumen['Articulos']}",
                  f"Cantidad de Enlaces: {resumen['Enlaces']}", 
                  "",
                  "Top 5 Grado Entrada:"]
        
        if topEntrada:
            for indice, item in enumerate(topEntrada, start = 1):
                lineas.append(f"{indice}. {item['nombre']} -> {item['valor']}")    
        else:
            lineas.append("Sin Datos.")
            
        lineas.append("")
        lineas.append("Top 5 Grado Salida:")
        
        if topSalida:
            for indice, item in enumerate(topSalida, start = 1):
                lineas.append(f"{indice}. {item['nombre']} -> {item['valor']}")
        else:
            lineas.append("Sin Datos.")
            
        rutaSalida.write_text("\n".join(lineas) + "\n", encoding = "utf-8")