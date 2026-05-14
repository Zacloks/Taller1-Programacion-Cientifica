from pathlib import Path

class ReporteBasico:
    
    def __init__(self, carpetaResultados = None):
        if carpetaResultados is None:
            self.carpetaResultados = Path(__file__).resolve().parent.parent.parent / "results"
        else:
            self.carpetaResultados = Path(carpetaResultados)

    def exportarResultados2(self, grafo, ranking, top_categorias, top_tamanio, camino, id_orig, id_dest):
        self.carpetaResultados.mkdir(parents=True, exist_ok=True)

        resumen = grafo.resumen()
        top_pagerank = sorted(ranking.items(), key=lambda x: x[1], reverse=True)[:10]

        lineas = ["Resultados Completos - Red de Wikipedia", "=" * 50,"", "=== Resumen del Grafo ===", 
                f"Artículos: {resumen['Articulos']}", f"Enlaces: {resumen['Enlaces']}", "","=== Top 10 por Grado de Entrada ===",]

        for i, nodo in enumerate(grafo.topPorGradoEntrada(10), start=1):
            nombre = nodo.nombre if nodo.nombre else str(nodo.id)
            lineas.append(f"  {i}. {nombre} -> {nodo.gradoEntrada()}")

        lineas += ["", "=== Top 10 por Grado de Salida ==="]
        for i, nodo in enumerate(grafo.topPorGradoSalida(10), start=1):
            nombre = nodo.nombre if nodo.nombre else str(nodo.id)
            lineas.append(f"  {i}. {nombre} -> {nodo.gradoSalida()}")

        lineas += ["", "=== Top 10 por PageRank ==="]
        for i, (id_nodo, score) in enumerate(top_pagerank, start=1):
            nodo = grafo.articulos[id_nodo]
            nombre = nodo.nombre if nodo.nombre else str(id_nodo)
            lineas.append(f"  {i}. {nombre} -> {score:.6f}")

        lineas += ["", "=== Top 10 Categorías por PageRank Promedio ==="]
        for cat, promedio, cant in top_categorias:
            lineas.append(f"  {cat}: {promedio:.6f} ({cant} artículos)")

        lineas += ["", "=== Top 10 Categorías por Cantidad de Artículos ==="]
        for nombre_cat, nodos in top_tamanio:
            lineas.append(f"  {nombre_cat}: {len(nodos)} artículos")

        lineas += ["", "=== Conectividad ==="]
        if camino:
            lineas.append(f"Camino {id_orig} -> {id_dest}: {' -> '.join(map(str, camino))}")
            lineas.append(f"Longitud: {len(camino) - 1} saltos")
        else:
            lineas.append(f"Sin camino entre {id_orig} y {id_dest}")

        ruta = self.carpetaResultados / "resultados_completos.txt"
        ruta.write_text("\n".join(lineas) + "\n", encoding="utf-8")
        
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
    
    def imprimirPorConsola(self, grafo, ranking, top_categorias, top_tamanio, camino, id_orig, id_dest):
        resumenGrafo = grafo.resumen()
        
        topEntrada = self.extraerTop(grafo.topPorGradoEntrada(10), "entrada")
        topSalida = self.extraerTop(grafo.topPorGradoSalida(10), "salida")
        
        print()
        print("Resumen del Grafo")
        print("-" * 50)
        
        print(f"Cantidad de Articulos: {resumenGrafo['Articulos']}")
        print(f"Cantidad de Enlaces: {resumenGrafo['Enlaces']}")
        
        self.imprimirTop("Top 10 por grado de Entrada", topEntrada)
        self.imprimirTop("Top 10 por grados de Salida", topSalida)
        
        print()
        print("Top 10 por PageRank")
        print("-" * 30)
        
        top_pagerank = sorted(ranking.items(), key=lambda x: x[1], reverse=True)[:10]
        for i, (id_nodo, score) in enumerate(top_pagerank, start=1):
            nodo = grafo.articulos[id_nodo]
            nombre = nodo.nombre if nodo.nombre else str(id_nodo)
            print(f"  {i}. {nombre} -> {score:.6f}")
        
        print()
        print("Top Categorias por PageRank")
        print("-" * 30)
        
        for cat, promedio, cant in top_categorias:
            print(f"  {cat}: {promedio:.6f} ({cant} artículos)")
            
        print()
        print("Top Categorias por Articulos")
        print("-" * 30)
        for nombre_cat, nodos in top_tamanio:
            print(f"  {nombre_cat}: {len(nodos)} artículos")
            
        print()
        print("Conectividad")
        print("-" * 30)
        
        if camino:
            print(f"Camino más corto: {' -> '.join(map(str, camino))}")
            print(f"Longitud del camino: {len(camino) - 1} saltos")
        else:
            print(f"No hay camino entre {id_orig} y {id_dest}")
        
        print()
        print("Distribucion")
        print("-" * 30)
        
        print(f"Cantidad de Articulos Analizados: {resumenGrafo['Articulos']}")
        print()
        
        print("Grados de Entrada")
        grafo.analizarDistribucionGrados(tipo="entrada")
        
        print()
        print("Grados de Salida")
        grafo.analizarDistribucionGrados(tipo="salida")
        
        print("\n" + "-" * 50)