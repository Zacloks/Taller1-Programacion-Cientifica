from src.loaders.cargarDatos import CargarDatos
from src.utilidades.reporte_basico import ReporteBasico
from src.utilidades.graficos import Graficos

def separador(titulo):
    print(f"\n{'='*10} {titulo} {'='*10}")

def main():
    separador("Iniciando procesamiento de artículos de Wikipedia")

    cargadorDatos = CargarDatos()
    grafo = cargadorDatos.cargarGrafo()
    
    #Definir Variables
    id_orig, id_dest = 1, 500
    camino = grafo.encontrarCaminosSimples(id_orig, id_dest)
    ranking = grafo.pageRank(iteraciones=15, damping=0.85)
    top_categorias = grafo.ranking_categorias(ranking, top_n=10)
    top_tamanio = sorted(grafo.categorias.items(), key=lambda x: len(x[1]), reverse=True)[:10]

    reporte = ReporteBasico()
    reporte.imprimirPorConsola(grafo, ranking, top_categorias, top_tamanio, camino, id_orig, id_dest)

    separador("Generando Gráficos")
    graficos = Graficos()
    graficos.generarTodos(grafo, ranking, top_categorias)

    separador("Exportando Resultados")
    reporte.exportarResultados2(grafo, ranking, top_categorias, top_tamanio, camino, id_orig, id_dest)
    print("--- Resultados exportados a results/resultados_completos.txt ---")

    separador("Proceso Finalizado")

if __name__ == "__main__":
    main()