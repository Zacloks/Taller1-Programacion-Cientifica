from src.loaders.cargarDatos import CargarDatos
from src.utilidades.reporte_basico import ReporteBasico
from src.utilidades.graficos import Graficos

def separador(titulo):
    print(f"\n{'='*10} {titulo} {'='*10}")

def main():
    separador("Iniciando procesamiento de artículos de Wikipedia")

    cargadorDatos = CargarDatos()
    grafo = cargadorDatos.cargarGrafo()
    resumen = grafo.resumen()
    print(f"=== Grafo cargado: {resumen['Articulos']} artículos | {resumen['Enlaces']} enlaces ===")

    separador("Métricas Básicas")
    reporte = ReporteBasico()
    reporte.imprimirPorConsola(grafo)
    reporte.generar(grafo)
    print("=== Reporte básico exportado a results/reporte_basico.txt ===")

    separador("Distribución de Grados de Entrada")
    grafo.analizarDistribucionGrados(tipo="entrada")

    separador("Distribución de Grados de Salida")
    grafo.analizarDistribucionGrados(tipo="salida")

    separador("Recorrido y Conectividad")
    id_orig, id_dest = 1, 500

    alcanzable = grafo.esAlcanzable(id_orig, id_dest)
    print(f"¿Es alcanzable {id_orig} -> {id_dest}? {alcanzable}")

    camino = grafo.encontrarCaminosSimples(id_orig, id_dest)
    if camino:
        print(f"Camino más corto: {' -> '.join(map(str, camino))}")
        print(f"Longitud del camino: {len(camino) - 1} saltos")
    else:
        print(f"No hay camino entre {id_orig} y {id_dest}")

    separador("PageRank")
    print("Calculando PageRank (iteraciones=15, damping=0.85)...")
    ranking = grafo.pageRank(iteraciones=15, damping=0.85)

    top_pagerank = sorted(ranking.items(), key=lambda x: x[1], reverse=True)[:10]
    print("\nTop 10 artículos por PageRank:")
    for i, (id_nodo, score) in enumerate(top_pagerank, start=1):
        nodo = grafo.articulos[id_nodo]
        nombre = nodo.nombre if nodo.nombre else str(id_nodo)
        print(f"  {i}. {nombre} -> {score:.6f}")

    separador("Análisis de Categorías")
    print("Analizando impacto por categorías...")
    top_categorias = grafo.ranking_categorias(ranking, top_n=10)

    print("\nTop 10 Categorías más influyentes (PageRank promedio):")
    for cat, promedio, cant in top_categorias:
        print(f"  {cat}: {promedio:.6f} ({cant} artículos)")

    print("\nTop 10 Categorías por cantidad de artículos:")
    top_tamanio = sorted(grafo.categorias.items(), key=lambda x: len(x[1]), reverse=True)[:10]
    for nombre_cat, nodos in top_tamanio:
        print(f"  {nombre_cat}: {len(nodos)} artículos")

    separador("Generando Gráficos")
    graficos = Graficos()
    graficos.generarTodos(grafo, ranking, top_categorias)

    separador("Exportando Resultados")
    _exportarResultados(grafo, ranking, top_categorias, top_tamanio, camino, id_orig, id_dest)
    print("=== Resultados exportados a results/resultados_completos.txt ===")

    separador("Proceso Finalizado")

def _exportarResultados(grafo, ranking, top_categorias, top_tamanio, camino, id_orig, id_dest):
    from pathlib import Path
    carpeta = Path(__file__).resolve().parent / "results"
    carpeta.mkdir(parents=True, exist_ok=True)

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

    ruta = carpeta / "resultados_completos.txt"
    ruta.write_text("\n".join(lineas) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()