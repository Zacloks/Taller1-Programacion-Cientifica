from src.cargarDatos import CargarDatos

def main():
    cargadorDatos = CargarDatos()
    grafo = cargadorDatos.cargarGrafo()

    #Ranking de Importancia de los Articulos
    ranking = grafo.pageRank()
    
if __name__ == "__main__":
    main()
