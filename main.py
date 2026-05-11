from src.cargarDatos import CargarDatos

def main():
    cargadorDatos = CargarDatos()
    grafo = cargadorDatos.cargarGrafo()

    #Ranking de Importancia de los Articulos
    ranking = grafo.pageRank()
    rankingOrdenado = sorted(ranking.items(), key = lambda x: x[1], reverse = True)
    
    print("--- Ranking PageRank ---")
    for idNodo, valor in rankingOrdenado[:10]:
        print(f"Articulo: {idNodo} | Puntaje: {valor}")
    
if __name__ == "__main__":
    main()
