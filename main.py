from src.cargarDatos import CargarDatos
from src.reporte_basico import reporteBasico

def main():
    print("--Iniciando procesamiento de datos de Wikipedia--")

    #El cargado de los datos
    cargadorDatos = CargarDatos()
    grafo = cargadorDatos.cargarGrafo()
    print(f"Grafo cargado: {grafo.cantidadArticulos()} artículos.")

    #PageRank 
    print("Calculando PageRank")
    ranking = grafo.pageRank(iteraciones=15)

    #Se Analizan las categorias
    print("Analizando impacto por categorías")
    top_categorias = grafo.ranking_categorias(ranking, top_n=10)

    #Caminos entre articulos
    id_orig, id_dest = 1, 500 
    camino = grafo.encontrarCaminosSimples(id_orig, id_dest)
    
    #Generar Reporte
    reporte = reporteBasico()
    reporte.imprimirPorConsola(grafo)
    
    print("\n--- Resultados Adicionales ---")
    if camino:
        print(f"Camino encontrado entre {id_orig} y {id_dest}: {' -> '.join(map(str, camino))}")
    else:
        print(f"No hay camino directo entre {id_orig} y {id_dest}")

    print("\nTop 10 Categorías más influyentes (Promedio PageRank):")
    for cat, promedio, cant in top_categorias:
        print(f"- {cat}: {promedio:.6f} ({cant} artículos)")

    print(f"\nProceso finalizado.")
    
if __name__ == "__main__":
    main()
