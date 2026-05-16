from src.loaders.cargarDatos import CargarDatos
from src.utilidades.reporte_general import ReporteGeneral
from src.utilidades.reporte_futbol import ReporteFutbol
from src.utilidades.graficos_general import Graficos
from src.utilidades.graficos_futbol import GraficosFutbol

def separador(titulo):
    print(f"\n{'='*10} {titulo} {'='*10}")

def main():
    separador("Iniciando procesamiento de artículos de Wikipedia")

    cargadorDatos = CargarDatos()
    grafo = cargadorDatos.cargarGrafo()

    # Definir Variables
    id_orig, id_dest = 1, 500
    camino = grafo.encontrarCamino(id_orig, id_dest)
    ranking = grafo.pageRank(iteraciones=15, damping=0.85)
    top_categorias = grafo.ranking_categorias(ranking, top_n=10)
    top_tamanio = sorted(grafo.categorias.items(), key=lambda x: len(x[1]), reverse=True)[:10]

    # Análisis de fútbol
    separador("Análisis de Fútbol")
    grafo_futbol = grafo.subGrafoFutbol()
    ranking_futbol = grafo_futbol.pageRank(iteraciones=15, damping=0.85)
    top_futbolistas = grafo_futbol.topFutbolistasPorPageRank(ranking_futbol, top_n=10)
    cats_grandes = grafo_futbol.categoriasFutbolMasGrandes(top_n=10)
    cats_influyentes = grafo_futbol.categoriasFutbolMasInfluyentes(ranking_futbol, top_n=10)
    comparacion = grafo_futbol.compararPageRankLocalVsGlobal(ranking, ranking_futbol, top_n=10)

    # Imprimir por consola
    reporte_general = ReporteGeneral()
    reporte_general.imprimirPorConsola(grafo, ranking, top_categorias, top_tamanio, camino, id_orig, id_dest)

    reporte_futbol = ReporteFutbol()
    reporte_futbol.imprimirPorConsola(grafo, ranking, grafo_futbol, ranking_futbol,
                                      top_futbolistas, cats_grandes, cats_influyentes, comparacion)

    # Generar gráficos
    separador("Generando Gráficos")
    graficos = Graficos()
    graficos.generarTodos(grafo, ranking, top_categorias)

    graficos_futbol = GraficosFutbol()
    graficos_futbol.generarTodos(top_futbolistas, cats_influyentes, comparacion)

    # Exportar resultados
    separador("Exportando Resultados")
    reporte_general.exportar(grafo, ranking, top_categorias, top_tamanio, camino, id_orig, id_dest)
    reporte_futbol.exportar(grafo, ranking, grafo_futbol, ranking_futbol,
                            top_futbolistas, cats_grandes, cats_influyentes, comparacion)

    separador("Proceso Finalizado")

if __name__ == "__main__":
    main()